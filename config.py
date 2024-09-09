import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://shun:ivnsfinfpibnsnfspm@localhost/archery_club_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    