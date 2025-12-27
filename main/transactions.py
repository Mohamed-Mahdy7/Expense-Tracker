"""Transactions Operaitons"""
from flask import current_app, redirect, render_template, request
from flask_jwt_extended import get_jwt_identity
from sqlalchemy import text
from main.models import Categories, Transactions
from . import db

def add_transaction():
    """POST to transactions records"""
    data = request.form.to_dict()
    user_id = int(get_jwt_identity())
    
    new_transaction = Transactions(
        user_id=user_id,
        category_id = data.get("category_id"),
        amount = data.get("amount"),
        description = data.get("description"),
        date = data.get("date"),
        transaction_type = data.get("transaction_type"),
    )
    db.session.add(new_transaction)
    db.session.commit()
    current_app.logger.info("New Transaction Addes Successfully")
    
    transactions = db.session.query(Transactions).filter_by(
        user_id=user_id).order_by(Transactions.date.desc()).all()
    
    return render_template("transaction.html", transactions=transactions)


def get_transaction():
    """GET transaction records"""
    user_id = int(get_jwt_identity())
    categories = Categories.query.all()
    transactions = Transactions.query.filter_by(user_id=user_id).order_by(
        Transactions.date.desc()).all()
    
    return render_template(
        "transaction.html", 
        categories=categories,
        transactions=transactions)

