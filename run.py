from app import create_app

#アプリケーションインスタンスを作成
app = create_app()

#スクリプトが直接実行された場合にのみアプリケーションを実行
if __name__ == '__main__':
    app.run()