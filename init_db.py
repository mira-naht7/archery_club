from app import create_app, db
from app.models import User, Equipment

#アプリケーションインスタンスを作成
app = create_app()

#アプリケーションコンテキスト内でデータベーステーブルを作成
with app.app_context():
    db.create_all()
    print("Database tables created.")