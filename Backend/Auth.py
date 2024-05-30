from flask import jsonify, Blueprint
from flask_jwt_extended import create_access_token

from extensions import db
from models import User


auth_bp = Blueprint('auth', __name__)


@auth_bp.route("/login_user", methods=["GET"])
def login_user(data):
    try:
        # Retrieve the username from the data
        username = data.get("username")

        # Retrieve the password from the data
        password = data.get("password")

        # Checks to make sure the username and password are provided, if not it throws an error 400
        if not all([username, password]):
            return jsonify({"status": "error", "message": "Missing required fields"}), 400

        # Checks database for matching username, if username not found, throws an error 400 and directs the user to
        # signup
        user = db.session.query(User).filter(User.username == username).first()
        if not user:
            return jsonify({"status": "error", "message": "Username not found, please signup"}), 400

        # Checks if the password matches the password linked to the username in the database, if not then throw an error 400
        if not user.check_password(password):
            return jsonify({"status": "error", "message": "Password incorrect"}), 400
        else:
            # If the password is correct log the user in and assign access token
            print(user.role)
            additional_claims = {"role": user.role}
            access_token = create_access_token(identity={"username": username}, additional_claims=additional_claims)
            print(access_token)
            return jsonify({"status": "success", "access_token": access_token}), 200

    except Exception as e:
        print(str(e))
        return jsonify({"status": "error", "message": str(e)}), 500

auth_actions = {
    "login_user": login_user,
}