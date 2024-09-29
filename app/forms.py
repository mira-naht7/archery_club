from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, HiddenField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional,  NumberRange
from app.models import Member
import os
from flask import current_app

#登録フォーム
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

#ログインフォーム
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

#備品追加フォーム
class EquipmentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('assembled_bow', '弓'),
        ('case', 'ケース'),
        ('arrow', '矢'),
        ('parts', 'パーツ'),
        ('other', 'その他備品')
    ], validators=[DataRequired()])
    condition = SelectField('Condition', choices=[
        ('new', '新品'),
        ('good', '良好'),
        ('poor', '悪い')
    ], validators=[DataRequired()])
    user = SelectField('User', coerce=int, validators=[Optional()])
    details = TextAreaField('Details')
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)], default=1)
    submit = SubmitField('備品を追加')
    def __init__(self, *args, **kwargs):
        super(EquipmentForm, self).__init__(*args, **kwargs)
        self.user.choices = [(0, 'なし')] + [(m.id, m.name) for m in Member.query.all()]

#備品編集フォーム
class EditEquipmentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('assembled_bow', '弓'),
        ('case', 'ケース'),
        ('arrow', '矢'),
        ('parts', 'パーツ'),
        ('other', 'その他備品')
    ], validators=[DataRequired()])
    condition = SelectField('Condition', choices=[
        ('new', '新品'),
        ('good', '良好'),
        ('poor', '悪い')
    ], validators=[DataRequired()])
    user = SelectField('User', coerce=int, validators=[Optional()])
    details = TextAreaField('Details')
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)], default=1)
    submit = SubmitField('Update Equipment')

    def __init__(self, *args, **kwargs):
        super(EditEquipmentForm, self).__init__(*args, **kwargs)
        self.user.choices = [(0, 'なし')] + [(m.id, m.name) for m in Member.query.all()]

#メンバー追加フォーム
class MemberForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('メンバーの追加')

#メンバー編集フォーム
class EditMemberForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Update')

#メンバー削除フォーム
class DeleteMemberForm(FlaskForm):
    submit = SubmitField('Delete')