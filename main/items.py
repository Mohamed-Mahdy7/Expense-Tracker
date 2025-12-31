"""Item Operations"""

from flask import abort, current_app, redirect, render_template, request, url_for
from flask_jwt_extended import get_jwt_identity
from main.models import Items
from . import db


def add_item():
    """POST to Items records"""
    data = request.form.to_dict()
    user_id = int(get_jwt_identity())
    name = data.get("name")
    if not name:
        return render_template("item.html", error="item name cannot be empty")

    try:
        new_item = Items(name=name, price=data["price"], user_id=user_id)
        db.session.add(new_item)
        db.session.commit()

        current_app.logger.info(f"New item Added Successfully: {new_item.name}")
        # Fetch updated Items list
        items = (
            db.session.query(Items)
            .filter_by(user_id=user_id)
            .order_by(Items.name)
            .all()
        )

        return render_template("item.html", items=items)
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"error adding new item: {str(e)}")
        return render_template(
            "error.html",
            title="Add item Failed",
            error=f"Can't Add item",
            details=str(e),
            back_url=url_for("main.item_details"),
        )


def get_item():
    """GET item records"""
    user_id = int(get_jwt_identity())
    items = (
        db.session.query(Items).filter_by(user_id=user_id).order_by(Items.name).all()
    )
    

    return render_template("item.html", user_id=user_id, items=items)


def get_one_item(id):
    """Get on record from item"""
    user_id = int(get_jwt_identity())
    item = Items.query.get_or_404(id)
    items = (
        db.session.query(Items).filter_by(user_id=user_id).order_by(Items.name).all()
    )
    user_id = int(get_jwt_identity())

    if item.user_id != user_id:
        current_app.logger.error(
            f"Unauthorize get attempt by user {user_id} on item {id}"
        )
        abort(403)

    return render_template("item_edit.html", item=item, items=items)


def update_item(id):
    """Update item record"""
    item = Items.query.get_or_404(id)
    data = request.form.to_dict()
    user_id = int(get_jwt_identity())

    if item.user_id != user_id:
        current_app.logger.error(
            f"Unauthorize get attempt by user {user_id} on item {id}"
        )
        abort(403)

    try:
        item.name = data.get("name", item.name)
        item.price = data.get("price", item.price)

        db.session.commit()
        current_app.logger.info("\nitem Updated Successfully!\n")
        return redirect(url_for("main.item_details"))

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error Updating item: {str(e)}")
        return render_template(
            "error.html",
            title="Update item Failed",
            error=f"Can't Update item",
            details=str(e),
            back_url=url_for("main.item_edit"),
        )


def delete_item(id):
    """Delete item record"""
    item = Items.query.get_or_404(id)
    related_transactions = item.transactions
    user_id = int(get_jwt_identity())

    if item.user_id != user_id:
        current_app.logger.warning(
            f"Unauthorized delete attempt by user {user_id} on item {id}"
        )
        abort(403)

    try:
        if related_transactions:
            current_app.logger.error(
                f"Can't delete item associated with transactions, Delete transactions first"
            )
            return render_template(
                "error.html",
                title="Delete item Failed",
                error=f"Can't delete item associated with transactions, Delete transactions first",
                back_url=url_for("main.item_details"),
            )

        db.session.delete(item)
        db.session.commit()
        current_app.logger.info(f"\nitem {id} deleted successfully\n")
        return redirect(url_for("main.item_details"))

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error deleting item {id}: {str(e)}")
        return render_template(
            "error.html",
            title="Delete item Failed",
            error=f"Can't delete item associated with transactions, Delete transactions first",
            back_url=url_for("main.item_details"),
        )
