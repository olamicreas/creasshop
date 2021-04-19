from wtforms import Form, BooleanField, StringField, PasswordField, validators
from email_validator import validate_email, EmailNotValidError
from wtforms.validators import DataRequired

class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=4, max=25)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address',  [validators.DataRequired(), validators.Email('invalid email format')])
    #email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')

    

class LoginForm(Form):
    email = StringField('Email Address', [validators.Email()])
    password = PasswordField('Password', validators=[validators.DataRequired()])