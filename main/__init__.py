from flask import Blueprint, Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
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
    
    return app