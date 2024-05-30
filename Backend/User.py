from flask import jsonify, Blueprint
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from datetime import datetime
from extensions import db
from models import User
from form import email_checker

user_bp = Blueprint('user', __name__)
blacklist = set()

from extensions import jwt


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    return jti in blacklist


@user_bp.route("/register_user", methods=["POST"])
def register_user(data):
    print("Received data:", data, flush=True)
    try:
        # Retrieve the username from the data
        username = data.get("username")
        # Checks if the username is already in use, if it is throw an error 400
        if db.session.query(User.username).filter(User.username == username).first():
            return jsonify({"status": "error", "message": "Username already in use"}), 400

        # Retrieve the password from the data
        password = data.get("password")

        # Retrieve the email from the data
        email = data.get("email")
        # Checks if the email is already in use, if it is throw an error 400
        if db.session.query(User.email).filter(User.email == email).first():
            return jsonify({"status": "error", "message": "Email already in use"}), 400

        # Retrieve the date of birth from the data and convert into datetime object
        DateOfBirth = data.get("DateOfBirth")
        DateOfBirth = datetime.strptime(DateOfBirth, "%d/%m/%Y")

        # Retrieve the role from the data
        role = data.get("role")
        # Retrieve the phone number from the data
        phone = data.get("phone")

        # Prints the processed data
        print("processed data:", username, password, email, DateOfBirth, phone, role, flush=True)
        # If a field is missing, throw an error 400
        if not all([username, password, email, DateOfBirth, phone, role]):
            return jsonify({"status": "error", "message": "Missing required fields"}), 400

        # Create a new User object
        new_user = User(username=username, password=password, email=email, DateOfBirth=DateOfBirth, phone=phone,
                        role=role)

        # Add the new User object to the session
        db.session.add(new_user)

        # Commit the session to save the changes to the database
        db.session.commit()
        access_token = create_access_token(identity={'username': username})
        return jsonify({"status": "success", "access_token": access_token}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@user_bp.route("/change_email", methods=["POST"])
@jwt_required()
def change_email(data):
    try:
        # Retrieve the current user's username
        current_user = get_jwt_identity()['username']
        # Retrieve and validate the new email from the data
        new_email = data.get('new_email')
        is_valid, message = email_checker(new_email)
        if not is_valid:
            return jsonify({"status": "error", "message": message}), 400
        # Find the current user in the database and replace the old email with the new email
        user = db.session.query(User).filter(User.username == current_user).first()
        user.email = new_email
        db.session.commit()
        return jsonify({"status": "success", "message": "Email updated successfully"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@user_bp.route("/change_account", methods=["POST"])
@jwt_required()
def change_password(data):
    # Retrieve the current user's username
    current_user = get_jwt_identity()['username']
    # Retrieve the current password from the data
    current_password = data.get('current_password')
    # Retrieve the new password from the data
    new_password = data.get('new_password')
    # Retrieve the confirmation of the new password from the data
    confirm_new_password = data.get('confirm_new_password')

    # If any fields are blank throw an error 400
    if not all([current_password, new_password, confirm_new_password]):
        return jsonify({"status": "error", "message": "All fields are required"}), 400

    # If the new password does not match with the confirmation of the new password then throw an error 400
    if new_password != confirm_new_password:
        return jsonify({"status": "error", "message": "New passwords do not match"}), 400

    # Check if the current user's password matches the inputted current password, throw an error 400 if not
    user = db.session.query(User).filter(User.username == current_user).first()

    if not user or not user.check_password(current_password):
        return jsonify({"status": "error", "message": "Current password is incorrect"}), 400

    # Update the password and commit to the database
    user.password = new_password
    db.session.commit()

    return jsonify({"status": "success", "message": "Password updated successfully"}), 200


@user_bp.route("/delete_account", methods=["POST"])
@jwt_required()
def delete_account(data):
    try:
        # Retrieve the current user's username
        current_user = get_jwt_identity()['username']
        print("Current user extracted:", )

        # Find the current user in the database
        user = db.session.query(User).filter(User.username == current_user).first()
        # If the user is found, delete the user from the database
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify({"status": "success", "message": "Account deleted successfully"}), 200
        else:
            # If the user is not found throw error 400
            return jsonify({"status": "error", "message": "User not found"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@user_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout(data):
    # Gets the user's token and invalidates it to log the user out
    print("Received data:", data)
    jti = get_jwt()['jti']
    print("JWT:", jti)
    blacklist.add(jti)
    return jsonify({"status": "success", "message": "Successfully logged out"}), 200


user_actions = {
    "register_user": register_user,
    "change_email": change_email,
    "change_password": change_password,
    "delete_account": delete_account,
    "logout": logout
}
