"""Category Operations"""
from http.client import TOO_EARLY
from flask import abort, current_app, redirect, render_template, request, url_for
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


def get_one_category(id):
    """Get on record from category"""
    category = Categories.query.get_or_404(id)
    categories = Categories.query.all()
    user_id = int(get_jwt_identity())
    
    if category.user_id != user_id:
        current_app.logger.error(f"Unauthorize get attempt by user {user_id} on category {id}")
        abort(403)
    
    return render_template(
        "category_edit.html",
        category=category,
        categories=categories
    )


def update_category(id):
    """Update category record"""
    category = Categories.query.get_or_404(id)
    data = request.form.to_dict()
    user_id = int(get_jwt_identity())
    
    if category.user_id != user_id:
        current_app.logger.error(f"Unauthorize get attempt by user {user_id} on category {id}")
        abort(403)
    
    try:
        if "name" in data:
            category.name = data["name"]
        
        category.price = data.get("price", category.price)
        
        db.session.commit()
        current_app.logger.info("\nCategory Updated Successfully!\n")
        return  redirect(url_for("main.category_details"))
    
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error Updating category: {str(e)}")
        return render_template(
            "category.html", 
            error=f"Error Updating category: {str(e)}")


def delete_category(id):
    """Delete category record"""
    category = Categories.query.get_or_404(id)
    user_id = int(get_jwt_identity())
    
    if category.user_id != user_id:
        current_app.logger.warning(
            f"Unauthorized delete attempt by user {user_id} on category {id}"
        )
        abort(403)
    
    try:
        db.session.delete(category)
        db.session.commit()
        current_app.logger.info(f"\ncategory {id} deleted successfully\n")
        return redirect(url_for("main.category_details"))
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error deleting category {id}: {str(e)}")
        return redirect(url_for("main.category_details", error=f"Error Deleting category: {str(e)}"))