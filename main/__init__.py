from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import Config

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    """Creating Flask app"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    jwt.init_app(app)
    
    @app.route("/")
    def hello():
        return "Working..."
    
    from auth import auth as auth_blueprint
    
    app.register_blueprint(auth_blueprint)
    
    return app