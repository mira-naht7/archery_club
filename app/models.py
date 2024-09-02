from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    condition = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('member.id', name='fk_equipment_user'), nullable=True)
    details = db.Column(db.Text)
    quantity = db.Column(db.Integer, default=1)
    user = db.relationship('Member', backref='equipment', lazy=True)

    @property
    def image_file(self):
        if self.category == 'assembled_bow':
            return 'default_bow.jpg'
        elif self.category == 'case':
            return 'default_case.png'
        elif self.category == 'arrow':
            return 'default_arrow.jpg'


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return f"Member('{self.name}')"
    
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))