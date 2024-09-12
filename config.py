import os
from dotenv import load_dotenv

load_dotenv()  # .envファイルから環境変数を読み込む

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    DATABASE_URL = os.getenv('DATABASE_URL') or os.getenv('DEV_DATABASE_URL')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or os.getenv('DEV_DATABASE_URL')
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_TRACK_MODIFICATIONS = False