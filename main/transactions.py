"""Transactions Operaitons"""
from datetime import datetime
from http.client import TOO_EARLY
from sre_constants import CATEGORY_UNI_DIGIT
from flask import abort, current_app, redirect, render_template, request, url_for
from flask_jwt_extended import get_jwt_identity
from sqlalchemy import text
from main.models import Categories, Transactions
from . import db

def add_transaction():
    """POST to transactions records"""
    data = request.form.to_dict()
    user_id = int(get_jwt_identity())
    category_id = data.get("category_id")
    category = Categories.query.get(category_id)
    price = category.price
    amount = float(data.get("amount"))
    total = price * amount
    
    try:
        new_transaction = Transactions(
            user_id = user_id,
            category_id = category_id,
            amount = amount,
            total = total,
            description = data.get("description"),
            date = datetime.strptime(data.get("date"), "%Y-%m-%d").date(),
            transaction_type = data.get("transaction_type"),
        )
        db.session.add(new_transaction)
        db.session.commit()
        current_app.logger.info("New Transaction Addes Successfully")
    except Exception as e:
        current_app.logger.error(f"Error adding new Transaction: {str(e)}")
        return render_template(
            "transaction.html", 
            error=f"Error adding new Transaction: {str(e)}")
    
    return get_transaction()


def get_transaction():
    """GET transaction records"""
    user_id = int(get_jwt_identity())
    categories = Categories.query.all()
    
    transactions = Transactions.query.filter_by(
        user_id=user_id).order_by(Transactions.date.desc()).all()
    
    return render_template(
        "transaction.html", 
        categories=categories,
        transactions=transactions)


def get_one_transaction(id):
    """GET one transaction record"""
    transaction = Transactions.query.get_or_404(id)
    categories = Categories.query.all()
    user_id = int(get_jwt_identity())
    
    if transaction.user_id != user_id:
        current_app.logger.warning(
            f"Unauthorized get attempt by user {user_id} on transaction {id}"
        )
        return redirect(url_for(
            "main.transaction_details", 
            error=f"Unauthorized get attempt by user {user_id} on transaction {id}"))
    
    return render_template(
        "transaction_edit.html", 
        transaction=transaction,
        categories=categories)


def update_transaction(id):
    """Update transaction record"""
    transaction = Transactions.query.get_or_404(id)
    data = request.form.to_dict()
    user_id = int(get_jwt_identity())
    
    if transaction.user_id != user_id:
        current_app.logger.warning(
            f"Unauthorized update attempt by user {user_id} on transaction {id}"
        )
        return redirect(url_for("main.transaction_details"))
    
    try:
        if "category_id" in data:
            transaction.category_id = int(data["category_id"])
            
        if "amount" in data:
            transaction.amount = float(data["amount"])
            
        if "date" in data and data["date"]:
            transaction.date = datetime.strptime(
                data["date"], "%Y-%m-%d"
            ).date()
            
        transaction.description = data.get("description", transaction.description)
        transaction.transaction_type = data.get(
            "transaction_type", transaction.transaction_type)
        
        category = Categories.query.get(transaction.category_id)
        transaction.total = transaction.amount * category.price
            
        db.session.commit()
        current_app.logger.info("\nTransaction Updated Successfully!\n")
        return  redirect(url_for("main.transaction_details"))
    
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error Updating Transaction: {str(e)}")
        return render_template(
            "transaction.html", 
            error=f"Error Updating Transaction: {str(e)}")


def delete_transaction(id):
    """Delete transaction record"""
    transaction = Transactions.query.get_or_404(id)
    user_id = int(get_jwt_identity())
    
    if transaction.user_id != user_id:
        current_app.logger.warning(
            f"Unauthorized delete attempt by user {user_id} on transaction {id}"
        )
        abort(403)
    
    try:
        db.session.delete(transaction)
        db.session.commit()
        current_app.logger.info(f"\nTransaction {id} deleted successfully\n")
        return redirect(url_for("main.transaction_details"))
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error deleting transaction {id}: {str(e)}")
        return redirect(url_for("main.transaction_details", error=f"Error Deleting transaction: {str(e)}"))