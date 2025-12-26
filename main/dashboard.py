"""Contain dashbord logic"""
from datetime import datetime
from sqlalchemy import text, func
from flask import current_app, render_template, request
from flask_jwt_extended import get_jwt_identity

from main.models import Categories, Transactions
from . import db


def dashboard():
    user_id = int(get_jwt_identity())
    
    now = datetime.now()
    month = request.args.get("month", f"{now.month:02}")
    year = request.args.get("year", str(now.year))
    
    #Total income
    income = db.session.query(db.func.coalesce(
        db.func.sum(Transactions.amount), 0)).filter(
        Transactions.user_id==user_id,
        Transactions.transaction_type=="income",
        db.extract("month", Transactions.date)==month,
        db.extract("year", Transactions.date)==year,
        ).scalar()
    
    #Total expenses
    expenses = db.session.query(db.func.coalesce(
        db.func.sum(Transactions.amount), 0)).filter(
        Transactions.user_id==user_id,
        Transactions.transaction_type=="expense",
        db.extract("month", Transactions.date)==month,
        db.extract("year", Transactions.date)==year,
        ).scalar()
    
    balance = income - expenses
    
    #Pie chart
    
    category_data = db.session.query(
        Categories.name,
        func.coalesce(func.sum(Transactions.amount), 0).label("total")
        ).join(Transactions, Categories.id==Transactions.category_id).filter(
        Transactions.user_id==user_id,
        Transactions.transaction_type=="expense",
        db.extract("month", Transactions.date)==month,
        db.extract("year", Transactions.date)==year,
    ).group_by(Categories.name).all()
    
    
    labels = [row["name"] for row in category_data]
    values = [row["total"] for row in category_data]
    
    return render_template(
        "dashboard.html",
        income=income,
        expenses=expenses,
        balance=balance,
        labels=labels,
        values=values,
        month=month,
        year=year
    )