from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    """Creating Flask app"""
    app = Flask(__name__)
    
    db.init_app(app)
    jwt.init_app(app)
    
    from main import main as main_blueprint
    from auth import auth as auth_blueprint
    
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)
    
    return app