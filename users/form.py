from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DateField, BooleanField, validators
from wtforms.validators import Email, EqualTo
from wtforms.validators import ValidationError
import re
from wtforms.validators import Length
from wtforms.validators import DataRequired

# makes sure that the password contains a number, uppercase and lower case letter and one symbol
def password_checker(password):
    if len(password) < 6:
        return False, "Password must be minimum 6 characters in length"
    if not re.search(r'(?=.*\d)', password):
        return False, "Password must contain at least one digit"
    if not re.search(r'(?=.*[a-zA-Z])', password):
        return False, "Password must contain at least one uppercase and one lowercase character"
    if not re.search(r'(?=.*\W)', password):
        return False, "Password must contain a symbol"
    return True


# makes sure the phone number is in Uk number format
def phone_checker(phone):
    p = re.compile(r'^(?:(?:\+|00)44|0) '
                   r'?(?:\d{4} ?\d{3} '
                   r'?\d{3}|\d{3} ?\d{4} '
                   r'?\d{4}|\d{5} '
                   r'?\d{4} '
                   r'?\d{2})$')
    if not p.match(phone.data):
        return False, "invalid phone number"
    return True

# makes sure the username cannot contain these symbols and is present
def username_checker(username):
    excluded_symbol = r'[!@#$%^&*()+=\[\]{};:\'"\\|,.<>?]'

    if any(char in excluded_symbol for char in username):
        return False, "invalid symbols"
    if not username:
        return False, "Please fill in this field"
    return True

def email_checker(email):
    p = re.compile(r'(?=.*[a-zA-Z0-9_.+-])'
                   r'(?=.*[@])(?=.*[a-zA-Z0-9-])'
                   r'(?=.*[.])(?=.*[a-zA-Z0-9-.])')
    if not p.match(email.data):
        return False, "invalid email"
    return True

def confirm_password_checker (password, confirm_password):
    if password != confirm_password:
        return False, "Passwords do not match."
    return True


def dob_checker(dob):
    p =re.compile(r'^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/[0-9]{4}$')
    if not p.match(dob.data):
        return False, "invalid phone number format try dd/mm/yyyy"
    return True

# form for the register page
class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), symbol_checker])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired(), phone_checker])
    dob = DateField('Date of Birth', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=12), password_checker])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo("password")])

    submit = SubmitField()

# form for the login page
class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])

    submit = SubmitField()

# form for changing the password
class PasswordForm(FlaskForm):
    current_password = PasswordField(id='password', validators=[DataRequired()])
    show_password = BooleanField('Show password', id='check')
    new_password = PasswordField(validators=[DataRequired(), Length(min=6, max=12), password_checker])
    confirm_new_password = PasswordField(validators=[DataRequired(), EqualTo('new_password')])

# form for changing the email
class EmailForm(FlaskForm):
    current_email = StringField(id='email' , validators=[DataRequired()])
    show_email = BooleanField('Show email', id='check')
    new_email = StringField(validators=[DataRequired(), Email()])
