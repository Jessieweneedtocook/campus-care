from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
import os
from dotenv import load_dotenv
from datetime import timedelta, datetime
from models import db, User
from form import email_checker, password_checker
import logging
from logging.handlers import RotatingFileHandler


load_dotenv()
# start the flask application
app = Flask(__name__)
CORS(app)
# Configure the app with a secretkey, database uri, and jwt variable token
app.config["JWT_SECRET_KEY"] = os.getenv('SECRET_KEY')
app.config['JWT_ALGORITHM'] = os.getenv('JWT_ALGORITHM')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(seconds=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600)))
# Initialize JWTManager with the Flask app
jwt = JWTManager(app)
# Initialize the database with the Flask app
db.init_app(app)
# Set for storing blacklisted (revoked) JWTs
blacklist = set()

# Print logging level and handlers for debugging
print(f"Logging level: {app.logger.level}")
print(f"Handlers: {app.logger.handlers}")


# from users.views import users_blueprint
# from admin.views import admin_blueprint

# app.register_blueprint(users_blueprint)
# app.register_blueprint(admin_blueprint)

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    return jti in blacklist


@app.route("/register_user", methods=["POST"])
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
        app.logger.warning(f"User logged in: {username}")
        app.logger.handlers[1].flush()
        return jsonify({"status": "success", "access_token": access_token}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/login_user", methods=["GET"])
def login_user(data):
    try:
        # Retrieve the username from the data
        username = data.get("username")

        # Retrieve the password from the data
        password = data.get("password")

        # Checks to make sure the username and password are provided, if not it throws an error 400
        if not all([username, password]):
            return jsonify({"status": "error", "message": "Missing required fields"}), 400

        # Checks database for matching username, if username not found, throws an error 400 and directs the user to signup
        user = db.session.query(User).filter(User.username == username).first()
        if not user:
            return jsonify({"status": "error", "message": "Username not found, please signup"}), 400

        # Checks if the password matches the password linked to the username in the database, if not then throw an error 400
        if not user.check_password(password):
            return jsonify({"status": "error", "message": "Password incorrect"}), 400
        else:
            access_token = create_access_token(identity={'username': username})
            app.logger.warning(f"User Logged in: {username}")
            # If the password is correct log the user in and assign access token
            print(user.role)
            additional_claims = {"role": user.role}
            access_token = create_access_token(identity={"username": username}, additional_claims=additional_claims)
            print(access_token)
            return jsonify({"status": "success", "access_token": access_token}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@jwt_required()
@app.route("/change_email", methods=["POST"])
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
        app.logger.warning(f"User changed email: {current_user}")
        return jsonify({"status": "success", "message": "Email updated successfully"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@jwt_required()
@app.route("/change_account", methods=["POST"])
def change_password(data):
    # Retrieve the current user's username
    current_user = get_jwt_identity()['username']
    # Retrieve the current password from the data
    current_password = data.get('current_password')
    # Retrieve the new password from the data
    new_password = data.get('new_password')
    # Retrieve the confirmation of the new password from the data
    confirm_new_password = data.get('confirm_new_password')
    is_valid, message = password_checker(new_password)
    if not is_valid:
        return jsonify({"status": "success", "message": message}), 400

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
    app.logger.warning(f"User changed password: {current_user}")
    return jsonify({"status": "success", "message": "Password updated successfully"}), 200

# Route to delete user's individual account, requires JWT
@jwt_required()
@app.route("/delete_account", methods=["POST"])
def delete_account(data):
    try:
        # get user from the database
        # Retrieve the current user's username
        current_user = get_jwt_identity()['username']
        print("Current user extracted:", )

        user = db.session.query(User).filter(User.username == current_user).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            app.logger.info(f"User deleted their account: {current_user}")
            return jsonify({"status": "success", "message": "Account deleted successfully"}), 200
        else:
            return jsonify({"status": "error", "message": "User not found"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/logout", methods=["POST"])
@jwt_required()
def logout(data):
    print("Received data:",data)
    jti = get_jwt()['jti']
    print("JWT:",jti)
    blacklist.add(jti)
    return jsonify({"status": "success", "message": "Successfully logged out"}), 200

@jwt_required()
@app.route("/admin_delete_account", methods=["DELETE"])
def admin_delete_account(data):
    try:
        # Retrieve the current user's username
        current_user = get_jwt_identity()['username']
        # Find the current user in the database
        user = db.session.query(User).filter(User.username == current_user).first()
        # If the user has the Admin role, then search the database for the user to delete
        if user.role == "Admin":
            deleted_user = data.get("delete_username")
            deleted_user = db.session.query(User).filter(User.username == deleted_user).first()
            # If the deleted user is found then delete the user from the database and commit the changes
            if deleted_user:
                db.session.delete(deleted_user)
                db.session.commit()
                return jsonify({"status": "success", "message": "Account deleted successfully"}), 200
            else:
                # If the user is not found then throw error 404
                return jsonify({"status": "success", "message": "Account not found"}), 404
        else:
            # If the user does not have the Admin role, then throw error 403
            return jsonify({"status": "error", "message": "Role required is admin"}), 403
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/view_users", methods = ["GET"])
@jwt_required()
def view_users(data):
    try:
        # Retrieve and extract all the usernames from the database
        users = db.session.query(User.username).all()
        usernames = [user.username for user in users]
        # Return a list of all usernames
        return jsonify({"status": "success","usernames": usernames})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

actions = {
    "register_user": register_user,
    "login_user": login_user,
    "logout": logout,
    "change_email": change_email,
    "change_password": change_password,
    "delete_account": delete_account,
    "admin_delete_account": admin_delete_account,
    "view_users": view_users,
}

@app.route("/api", methods=["POST", "GET"])
def api():
    data = request.json
    print("received data:", data, flush=True)
    action = data.get("action")

    if action in actions:
        return actions[action](data)
    else:
        return jsonify({'status': 'error', 'message': 'Invalid action'}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
