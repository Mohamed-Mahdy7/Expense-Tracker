"""Contain dashbord logic"""

from datetime import datetime, date
from sqlalchemy import func
from flask import render_template, request
from flask_jwt_extended import get_jwt_identity
from main.models import Items, Transactions
from . import db


def dashboard():
    user_id = int(get_jwt_identity())
    # Date range 
    today = date.today()
    from_date_str = request.args.get("from")
    to_date_str = request.args.get("to")

    if from_date_str:
        from_date = datetime.strptime(from_date_str, "%Y-%m-%d").date()
    else:
        from_date = today.replace(day=1)

    if to_date_str:
        to_date = datetime.strptime(to_date_str, "%Y-%m-%d").date()
    else:
        to_date = today
    
    date_filter = (
        Transactions.date >= from_date,
        Transactions.date <= to_date
    )
    
    selected_type = request.args.get("type", "both")
    
    income = expenses = 0
    
    if selected_type in ("both", "income"):
    
        # Total income
        income = (
            db.session.query(func.coalesce(db.func.sum(Transactions.total), 0))
            .filter(
                Transactions.user_id == user_id,
                Transactions.transaction_type == "income",
                *date_filter
            )
            .scalar()
        )
    
    if selected_type in ("both", "expense"):
        
        # Total expenses
        expenses = (
            db.session.query(func.coalesce(db.func.sum(Transactions.total), 0))
            .filter(
                Transactions.user_id == user_id,
                Transactions.transaction_type == "expense",
                *date_filter
            )
            .scalar()
        )

    balance = income - expenses

    # Pie chart
    pie_labels = []
    pie_values = []
    
    pie_chart = (
        db.session.query(
            Items.name,
            func.coalesce(func.sum(Transactions.amount), 0).label("total"),
        )
        .join(Transactions, Items.id == Transactions.item_id)
        .filter(
            Transactions.user_id == user_id,
            *date_filter
        )
    )
    
    if selected_type != "both":
        pie_chart = pie_chart.filter(
        Transactions.transaction_type == selected_type
    )

    pie_data = pie_chart.group_by(Items.name).all()

    pie_labels = [row[0] for row in pie_data]
    pie_values = [row[1] for row in pie_data]
    
    # Bar Chart
    bar_labels = []
    bar_values = []

    if selected_type == "both":
        bar_labels = ["Income", "Expenses"]
        bar_values = [income, expenses]

    else:
        bar_query = (
        db.session.query(
            Items.name,
            func.coalesce(func.sum(Transactions.amount), 0).label("total"),
        )
        .join(Transactions, Items.id == Transactions.item_id)
        .filter(
            Transactions.user_id == user_id,
            Transactions.transaction_type == selected_type,
            *date_filter
        )
        .group_by(Items.name)
        .all()
    )
        
        bar_labels = [row[0] for row in bar_query]
        bar_values = [row[1] for row in bar_query]

    return render_template(
        "dashboard.html",
        income=income,
        expenses=expenses,
        balance=balance,
        pie_labels=pie_labels,
        pie_values=pie_values,
        bar_labels=bar_labels,
        bar_values=bar_values,
        from_date=from_date,
        to_date=to_date,
        selected_type=selected_type
    )
