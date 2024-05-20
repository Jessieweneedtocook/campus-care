import requests
from flask import Blueprint, jsonify

from backend import app
from users.form import SignupForm

users_blueprint = Blueprint('users', __name__, template_folder='templates')

@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    data = requests.json


