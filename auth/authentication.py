from flask import jsonify, current_app, request
from ..main.models import Users

def login():
    """log users in"""
    data = request.get_json()
    if not data or not data.get("username") or not data.get("hash"):
        current_app.logger.error("Invalid input: username and password required!")
        return jsonify({"error": "Invalid input: username and password required!"}), 400