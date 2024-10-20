import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database/todo_app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret_key_for_csrf_protection'
