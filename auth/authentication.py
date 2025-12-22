from flask import jsonify, current_app, make_response, render_template, request
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies
from werkzeug.security import check_password_hash, generate_password_hash

def login():
    """log users in"""
    from main.models import Users, db
    
    if request.method == "POST":
        data = request.get_json()
        if not data or not data.get("username") or not data.get("hash"):
            current_app.logger.error("Invalid input: username and password required!")
            return jsonify({"error": "Invalid input: username and password required!"}), 400
        
        username = data.get("username").strip()
        password = data.get("hash").strip()
        confirm_password = data.get("confirm_password").strip()
        
        user = db.session.query(Users).filter(Users.username==username).first()
        if not user:
            current_app.logger.error("User Not Found")
            return jsonify({"error": ""}), 404
        
        hash_password = generate_password_hash(password)
        
        try:
            stored_password = user.hash
            if hash_password == stored_password:
                # Create tokens
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(identity=user.id)
                
                response = make_response(jsonify({
                    "message": "Logged in Successfully!",
                    "User Name": user.username
                }))
                
                # Set Cookies
                set_access_cookies(response, access_token)
                response.set_cookie(
                    key="refresh_token_cookie",
                    value=refresh_token,
                    httponly=True,
                    samesite="Lax",
                    secure=False
                )
                return response, 200
            else:
                raise ValueError("wrong password, please try again")
        except Exception as e:
            current_app.logger.error(f"Error Logging in: {str(e)}")
            return jsonify({"error": "Error Logging in",
                            "detials": str(e)}), 500
            
    elif request.method == "GET":
        return render_template("login.html")