from flask import jsonify, current_app, make_response, redirect, render_template, request
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from werkzeug.security import check_password_hash, generate_password_hash
from main.models import Users, db
from datetime import datetime, timezone


def register():
    """Register users"""
    data = request.form.to_dict()
    if request.method == "POST":
        try:
            hash = data.get("password")
            confirm_password = data.get("confirm_password")
            
            if hash != confirm_password:
                return jsonify({
                    "error": "Password and Confirmation Password not the same!"
                    }), 400
            hash_password = generate_password_hash(hash)
            
            new_user = Users(
                username = data.get("username"),
                email = data.get("email"),
                hash = hash_password,
                created_at = datetime.now(timezone.utc)
            )
            db.session.add(new_user)
            db.session.commit()
            
            current_app.logger.info("Successfully Registerd!")
            return redirect("/login")
        except Exception as e:
            current_app.logger.error(f"Error Registering!: {str(e)}")
            return jsonify({"error": "Error Registering!",
                            "details": str(e)}), 500
    
    else:
        return render_template("register.html")


def login():
    """log users in"""
    if request.method == "POST":
        data = request.form.to_dict()
        if not data or not data.get("username") or not data.get("password"):
            current_app.logger.error("Invalid input: username and password required!")
            return jsonify({"error": "Invalid input: username and password required!"}), 400
        
        username = data.get("username").strip()
        password = data.get("password").strip()
        
        
        user = db.session.query(Users).filter(Users.username==username).first()
        if not user:
            current_app.logger.error("User Not Found")
            return jsonify({"error": ""}), 404
        
        hash_password = user.hash
        checked_password = check_password_hash(hash_password, password)
        
        try:
            hash_password = user.hash
            additional_claims={
                    "username": user.username,
                    "email": user.email
                }
            # Create tokens
            access_token = create_access_token(
                identity=str(user.id),
                fresh=True,
                additional_claims=additional_claims
                )
            refresh_token = create_refresh_token(
                identity=str(user.id),
                additional_claims=additional_claims
                )
            
            response = redirect("/dashboard")
            
            # Set Cookies
            response.set_cookie(
                "access_token_cookie", access_token,
                httponly=True,
                secure=False,
                samesite="Lax",
            )
            response.set_cookie(
                "refresh_token_cookie", refresh_token,
                httponly=True,
                samesite="Lax",
                secure=False
            )
            return response
        except Exception as e:
            current_app.logger.error(f"Error Logging in: {str(e)}")
            return jsonify({"error": "Error Logging in",
                            "detials": str(e)}), 500
            
    else:
        return render_template("login.html")


@jwt_required(refresh=True)
def refresh():
    """refresh cookies"""
    identity = get_jwt_identity()
    new_access_token = create_access_token(identity=identity)
    
    response = make_response(jsonify({
        "message": "Token Refreshed!",
        "access_token_cookie": new_access_token
    }), 201)
    
    response.set_cookie(
        "access_token_cookie", new_access_token,
        httponly=True,
        secure=False,
        samesite="Lax",
    )
    return response


@jwt_required()
def logout():
    response = make_response(jsonify({"message": "Logged out successfully!"}), 200)
    response.set_cookie(
        "access_token", "",
        expires=0, 
        httponly=True, 
        samesite="Lax"
        )
    response.set_cookie(
        "refresh_token", "",
        expires=0, 
        httponly=True, 
        samesite="Lax")
    return response