
from wtforms import Form, StringField, TextAreaField, PasswordField, SubmitField, validators
from email_validator import validate_email, EmailNotValidError
from flask_wtf.file import FileRequired, FileAllowed, FileField
from wtforms.validators import DataRequired, ValidationError
from .models import Register
from flask_wtf import FlaskForm


class CustomerRegistrationForm(FlaskForm):
    name = StringField('Name:', [validators.DataRequired()])
    username = StringField('Username:', [validators.DataRequired()])
    email = StringField('Email Address:', [validators.DataRequired(), validators.Email('Invalid Email address')])
    password = PasswordField('New Password:', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message=('Passwords must match'))
    ])
    confirm = PasswordField('Repeat Passwrod')
    country = StringField('Country', [validators.DataRequired()])
    state = StringField('State', [validators.DataRequired()])
    city = StringField('City', [validators.DataRequired()])
    address = StringField('Address', [validators.DataRequired()])
    contact = StringField('Conatact', [validators.DataRequired()])
    zipcode = StringField('Zip code', [validators.DataRequired()])

    profile = FileField('Profile', validators=[FileRequired(),FileAllowed(['jpeg', 'png', 'gif', 'jpg'], 'Images only')])
    


    def validate_username(self, username):
        if Register.query.filter_by(username=username.data).first():
            raise ValidationError("This username has been taken")

    def validate_email(self, email):
        if Register.query.filter_by(email=email.data).first():
            raise ValidationError("This email is for another user")


class LoginForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])
