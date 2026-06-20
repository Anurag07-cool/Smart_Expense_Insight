import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'super_secret_key_development_only')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///smart_expense.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REPORTS_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'reports')

    @staticmethod
    def init_app(app):
        # Create reports folder if it doesn't exist
        if not os.path.exists(Config.REPORTS_FOLDER):
            os.makedirs(Config.REPORTS_FOLDER)
