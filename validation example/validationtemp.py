import re

def validate_username(username):
    excluded_symbols = r'[!@#$%^&*()+=\[\]{};:\'"\\|,.<>?]'
    if any(char in excluded_symbols for char in username):
        return False, "Username contains invalid symbols."
    if not username:
        return False, "Username cannot be empty."
    return True, ""

def validate_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, email):
        return False, "Invalid email address."
    return True, ""

def validate_phone(phone):
    phone_regex = r'^(?:(?:\+|00)44|0)?(?:\d{4} ?\d{3} ?\d{3}|\d{3} ?\d{4} ?\d{4}|\d{5} ?\d{4} ?\d{2})$'
    if not re.match(phone_regex, phone):
        return False, "Invalid phone number format."
    return True, ""

def validate_password(password):
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit."
    if not re.search(r'[a-zA-Z]', password):
        return False, "Password must contain at least one letter."
    if not re.search(r'\W', password):
        return False, "Password must contain at least one symbol."
    return True, ""

def validate_confirm_password(password, confirm_password):
    if password != confirm_password:
        return False, "Passwords do not match."
    return True, ""