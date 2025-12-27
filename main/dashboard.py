"""Contain dashbord logic"""
from datetime import datetime
from sqlalchemy import Integer, cast, text, func
from flask import current_app, render_template, request
from flask_jwt_extended import get_jwt_identity

from main.models import Categories, Transactions
from . import db


def dashboard():
    user_id = int(get_jwt_identity())
    month_str = request.args.get("month")
    if month_str:
        year, month = map(int, month_str.split("-"))
    else:
        now = datetime.now()
        month = request.args.get("month", f"{now.month:02}")
        year = request.args.get("year", str(now.year))
    
    #Total income
    income = db.session.query(func.coalesce(
        db.func.sum(Transactions.amount), 0)).filter(
        Transactions.user_id==user_id,
        Transactions.transaction_type=="income",
        cast(func.strftime('%Y', Transactions.date), Integer) == year,
        cast(func.strftime('%m', Transactions.date), Integer) == month,
        ).scalar()
    
    #Total expenses
    expenses = db.session.query(func.coalesce(
        db.func.sum(Transactions.amount), 0)).filter(
        Transactions.user_id==user_id,
        Transactions.transaction_type=="expense",
        cast(func.strftime('%m', Transactions.date), Integer) == month,
        cast(func.strftime('%Y', Transactions.date), Integer) == year,
        ).scalar()
    
    balance = income - expenses
    
    #Pie chart
    category_data = db.session.query(
        Categories.name,
        func.coalesce(func.sum(Transactions.amount), 0).label("total")
        ).join(
            Transactions, Categories.id==Transactions.category_id
        ).filter(
        Transactions.user_id==user_id,
        Transactions.transaction_type=="expense",
        cast(func.strftime('%m', Transactions.date), Integer) == month,
        cast(func.strftime('%Y', Transactions.date), Integer) == year,
    ).group_by(Categories.name).all()
    
    
    labels = [row[0] for row in category_data]
    values = [row[1] for row in category_data]
    
    return render_template(
        "dashboard.html",
        income=income,
        expenses=expenses,
        balance=balance,
        labels=labels,
        values=values,
    )