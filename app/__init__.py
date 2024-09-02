from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from config import Config
from dotenv import load_dotenv
import os


load_dotenv() 

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'login'
csrf = CSRFProtect()
migrate = Migrate()

def create_app():
    app = Flask(__name__, static_folder='static', static_url_path='/static')
    app.config.from_object(Config)
    
    def create_directories():
        directories = [
            os.path.join(app.root_path, 'static'),
            os.path.join(app.root_path, 'static', 'equipment_pics'),
        ]
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)

    # アプリケーション起動時にディレクトリを作成
    with app.app_context():
        create_directories()

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    from app import routes
    routes.init_routes(app)



    return app