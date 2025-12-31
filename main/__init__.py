from flask import Blueprint, Flask, flash, g, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, set_access_cookies, verify_jwt_in_request
from flask_jwt_extended.exceptions import NoAuthorizationError
from jwt import ExpiredSignatureError
from config import Config

db = SQLAlchemy()
jwt = JWTManager()


main = Blueprint("main", __name__, template_folder="templates")
from . import routes

def create_app():
    """Creating Flask app"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    jwt.init_app(app)
    
    @app.route("/")
    def hello():
        return render_template("landing.html")
    
    from auth import auth as auth_blueprint
    from main import main as main_blueprint
    
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    
    @app.before_request
    def auto_refresh_access_token():
        # Skip public routes
        if request.path in ("/", "/login", "/register") or request.path.startswith("/static"):
            return

        g.user_id = None
        g.new_access_token = None

        try:
            verify_jwt_in_request(optional=True)  # allows expired
            identity = get_jwt_identity()
            if identity:
                g.user_id = int(identity)
                return
        except Exception:
            pass  # expired token, continue to refresh

        # Access token expired → try refresh token
        try:
            verify_jwt_in_request(refresh=True)  # verifies refresh token properly
            identity = get_jwt_identity()
            g.user_id = int(identity)
            g.new_access_token = create_access_token(identity=identity)
            return redirect(request.path)
        except NoAuthorizationError:
            flash("Unauthorized request. Please login again.", "warning")
            return redirect(url_for("auth.login_"))
        except ExpiredSignatureError:
            return render_template("error.html", error="Refresh token expired"), 401

    @app.after_request
    def set_new_access_cookie(response):
        if g.get("new_access_token"):
            set_access_cookies(response, g.new_access_token)
        return response
    
    return app