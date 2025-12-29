"""Category Operations"""
from flask import current_app, render_template, request
from flask_jwt_extended import get_jwt_identity
from main.models import Categories
from . import db


def add_category():
    """POST to categories records"""
    data = request.form.to_dict()
    user_id = int(get_jwt_identity())
    name = data.get("name")
    if not name:
        return render_template("category.html", error="Category name cannot be empty")
    
    new_category = Categories(
        name = name,
        price = data['price'],
        user_id = user_id
    )
    db.session.add(new_category)
    db.session.commit()
    
    current_app.logger.info(f"New Category Added Successfully: {new_category.name}")
    # Fetch updated categories list
    categories = db.session.query(Categories).filter_by(
        user_id=user_id).order_by(Categories.name).all()
    
    return render_template("category.html", categories=categories)


def get_category():
    """GET category records"""
    user_id = int(get_jwt_identity())
    categories = db.session.query(Categories).filter_by(
        user_id=user_id).order_by(Categories.name).all()
    
    return render_template("category.html", user_id=user_id, categories=categories)