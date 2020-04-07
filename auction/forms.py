from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, StringField,SubmitField,BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from auction.models import User

class registerForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=4, max=15)])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sing in')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken.')

class loginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class updateAccountForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=4, max=15)])
    email = StringField('email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken.')