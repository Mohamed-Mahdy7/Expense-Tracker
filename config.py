from datetime import  timedelta

import os, datetime
from dotenv import load_dotenv

load_dotenv(".env")

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Make configraiton settings"""
    
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = ("sqlite:///" + os.path.join(BASE_DIR, "instance", "sqlite.db"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    DEBUG = True
    FLASK_JWT_SECRET_KEY = os.getenv("FLASK_JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_ACCESS_TOKEN_NAME = "access_token_cookie"
    JWT_REFRESH_TOKEN_NAME = "refresh_token_cookie"
    JWT_COOKIE_CSRF_PROTECT = False  
    JWT_COOKIE_SECURE = False        
    JWT_COOKIE_SAMESITE = "Lax"