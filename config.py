import os
from dotenv import load_dotenv

#.envファイルから環境変数を読み込む
load_dotenv()

class Config:
    #アプリケーションの秘密鍵（セッション管理などに使用）
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    
    #データベースURLの設定
    #本番環境のDATABASE_URLか開発環境のDEV_DATABASE_URLを使用
    DATABASE_URL = os.getenv('DATABASE_URL') or os.getenv('DEV_DATABASE_URL')
    
    #HerokuのPOSTGRESQLアドドンに対応するためのURL変換
    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    
    #SQLAlchemyの設定
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # パフォーマンス向上のため、変更トラッキングを無効化