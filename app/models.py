from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

#ユーザーモデル
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, index=True, unique=True) 
    password_hash = db.Column(db.Text) 

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
#備品モデル
class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    condition = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('member.id', name='fk_equipment_user'), nullable=True)
    details = db.Column(db.Text)
    quantity = db.Column(db.Integer, default=1)
    user = db.relationship('Member', backref='equipment', lazy=True)

    @property #備品の画像を返す
    def image_file(self):
        if self.category == 'assembled_bow':
            return 'default_bow.jpg'
        elif self.category == 'case':
            return 'default_case.png'
        elif self.category == 'arrow':
            return 'default_arrow.jpg'

#メンバーモデル
class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return f"Member('{self.name}')"
    
#ユーザーロード
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))