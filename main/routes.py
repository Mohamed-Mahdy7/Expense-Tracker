from flask import render_template
from flask_jwt_extended import jwt_required
from . import main
from .dashboard import dashboard


@main.route("/home")
def home():
    return render_template("home.html")

@main.route("/dashboard")
@jwt_required()
def dashboard_():
    return dashboard()