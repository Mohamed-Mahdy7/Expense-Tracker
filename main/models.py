from enum import unique
from sqlalchemy import CheckConstraint, ForeignKey
from . import db


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    hash = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime)
    users = db.relationship("Transactions", back_populates="user")



class Categories(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey("users.id"))
    transactions = db.relationship("Transactions", back_populates="category")


class Transactions(db.Model):
    __tablename__ = "transactions"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("users.id"))
    category_id = db.Column(db.Integer, ForeignKey("categories.id"))
    amount = db.Column(db.Float)
    description = db.Column(db.Text)
    date = db.Column(db.Text)
    transaction_type = db.Column(db.Text)
    user = db.relationship("Users", back_populates="users")
    category = db.relationship("Categories", back_populates="transactions")
    
    __table_args__ = (
        CheckConstraint(
            "transaction_type IN ('income', 'expense')", name="check_type_valid"
        ),
    )