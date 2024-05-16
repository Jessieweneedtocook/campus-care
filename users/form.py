from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DateField, BooleanField, validators
from wtforms.validators import Email, EqualTo
from wtforms.validators import ValidationError
import re
from wtforms.validators import Length
from wtforms.validators import DataRequired

def password_checker(form, password):
    p = re.compile(r'(?=.*\d)(?=.*[a-zA-Z])(?=.*\W)')
    if not p.match(password.data):
        raise ValidationError()

def phone_checker(form, phone):
    p = re.compile(r'^(?:(?:\+|00)44|0) '
                   r'?(?:\d{4} ?\d{3} '
                   r'?\d{3}|\d{3} ?\d{4} '
                   r'?\d{4}|\d{5} '
                   r'?\d{4} '
                   r'?\d{2})$')
    if not p.match(phone.data):
        raise ValidationError()

class SignupForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    email = StringField(validators=[DataRequired(), Email()])
    phone = StringField(validators=[DataRequired()])
    dob = DateField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired(), Length(min=6, max=12)])
    confirm_password = PasswordField(validators=[DataRequired(), EqualTo("password")])

    submit = SubmitField()
