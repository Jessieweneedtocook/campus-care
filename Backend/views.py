import requests
from flask import Blueprint, jsonify

from Backend.form import SignupForm

users_blueprint = Blueprint('users', __name__, template_folder='templates')

@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    data = requests.json
    form = SignupForm(data=data)

    if form.validate():
        username = form.username.data
        email = form.email.data
        phone = form.phone.data
        dob = form.dob.data
        password = form.password.data

        return jsonify({"message": "User registered successfully"}), 201
    else:
        errors = form.errors
        return jsonify({"message": "Validation failed", "errors": errors}), 400


