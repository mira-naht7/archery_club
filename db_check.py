from app import create_app, db
from app.models import User, Equipment
from sqlalchemy import inspect

app = create_app()
app.app_context().push()

# データベース内のテーブルを表示
inspector = inspect(db.engine)
print(inspector.get_table_names())

# Userテーブルの内容を確認
print("Users:")
users = User.query.all()
for user in users:
    print(f"ID: {user.id}, Username: {user.username}")

# Equipmentテーブルの内容を確認
print("\nEquipment:")
equipment = Equipment.query.all()
for item in equipment:
    print(f"ID: {item.id}, Name: {item.name}, Type: {item.type}, Condition: {item.condition}, Owner: {item.owner}")

# セッションを閉じる
db.session.close()