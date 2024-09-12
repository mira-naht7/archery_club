import os
from dotenv import load_dotenv

load_dotenv()  # .envファイルから環境変数を読み込む

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    DATABASE_URL = os.getenv('DATABASE_URL') or os.getenv('DEV_DATABASE_URL')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or os.getenv('DEV_DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False