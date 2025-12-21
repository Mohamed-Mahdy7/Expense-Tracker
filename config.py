import os
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