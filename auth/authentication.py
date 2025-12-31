from flask import flash, jsonify, current_app, redirect, render_template, request, url_for
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, set_access_cookies, set_refresh_cookies, verify_jwt_in_request
from flask_jwt_extended.exceptions import NoAuthorizationError
from werkzeug.security import check_password_hash, generate_password_hash
from main.models import Users, db
from datetime import datetime, timezone
from . import auth


def register():
    """Register users"""
    data = request.form.to_dict()
    if request.method == "POST":
        try:
            hash = data.get("password")
            confirm_password = data.get("confirm_password")
            
            if hash != confirm_password:
                return render_template(
                "error.html",
                title = "Register Error",
                error="Password and Confirmation Password not the same!",
                back_url=url_for("auth.register_"))
            
            new_user = data.get("username")
            existing_user = db.session.query(Users).filter(
                Users.username==new_user).first()
            
            if existing_user:
                return render_template(
                "error.html", 
                title = "Register Error",
                error="username already exists",
                back_url=url_for("auth.register_"))
                
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
            return render_template(
                "error.html", 
                title = "Register Error",
                error= str(e),
                back_url=url_for("auth.register_"))
    
    else:
        return render_template("register.html")


def login():
    """log users in"""
    if request.method == "POST":
        data = request.form.to_dict()
        if not data or not data.get("username") or not data.get("password"):
            current_app.logger.error("Invalid input: username and password required!")
            return render_template(
                "error.html", 
                title = "Invalid input",
                error="username and password required!",
                back_url=url_for("auth.login_"))
        
        username = data.get("username").strip()
        password = data.get("password").strip()
        
        user = db.session.query(Users).filter(Users.username==username).first()
        if not user:
            current_app.logger.error("User Not Found")
            return render_template(
                "error.html", 
                title = "Login Error",
                error="User Not Fount",
                back_url=url_for("auth.login_"))
        
        hash_password = user.hash
        checked_password = check_password_hash(hash_password, password)
        if not checked_password:
            return render_template(
                "error.html", 
                title = "Login Error",
                error="incorrect usename or password",
                back_url=url_for("auth.login_"))
        
        try:
            hash_password = user.hash
            additional_claims={
                    "username": user.username,
                    "email": user.email
                }
            # Create tokens
            access_token = create_access_token(
                identity=str(user.id),
                additional_claims=additional_claims
                )
            refresh_token = create_refresh_token(
                identity=str(user.id),
                additional_claims=additional_claims
                )
            
            response = redirect("/dashboard")
            
            # Set Cookies
            set_access_cookies(response, access_token)
            set_refresh_cookies(response, refresh_token)
            
            return response
        except Exception as e:
            current_app.logger.error(f"Error Logging in: {str(e)}")
            return render_template(
                "error.html", 
                title = "Login error",
                error=str(e),
                back_url=url_for("auth.login_"))
            
    else:
        return render_template("login.html")


def refresh():
    """refresh tokens"""
    try:
        identity = get_jwt_identity()
        new_access_token = create_access_token(identity=identity)
        
        response = jsonify({"message": "Token Refreshed!"})
        set_access_cookies(response, new_access_token)
        return response
    except NoAuthorizationError:
        return jsonify({"msg": "Refresh token is missing or invalid"}), 401


def logout():
    if request.method == "POST":
        flash("Logged out successfully", "info")
        response = redirect(url_for('auth.login_'))
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        response.set_cookie(
            "access_token_cookie", "",
            expires=0, 
            httponly=True, 
            samesite="Lax"
            )
        response.set_cookie(
            "refresh_token_cookie", "",
            expires=0, 
            httponly=True, 
            samesite="Lax")
        return response
    else:
        return render_template(
            "logout.html", 
            message=f"Are you sure you want to logout?",
            back_url=url_for("main.dashboard_"))
