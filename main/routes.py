from flask import render_template, request
from flask_jwt_extended import jwt_required
import jwt
from . import main
from .dashboard import dashboard
from .transactions import add_transaction, get_transaction
from .categories import add_category, get_category


@main.route("/home")
def home():
    return render_template("home.html")

@main.route("/dashboard")
@jwt_required()
def dashboard_():
    return dashboard()


@main.route("/transactions", methods=["GET", "POST"])
@jwt_required()
def transaction_details():
    if request.method == 'POST':
        return add_transaction()
    else:
        return get_transaction()


@main.route("/categories", methods=["GET", "POST"])
@jwt_required()
def category_details():
    if request.method == "POST":
        return add_category()
    else:
        return get_category()

