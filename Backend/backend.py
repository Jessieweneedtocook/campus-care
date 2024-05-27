from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
import os
from dotenv import load_dotenv
from datetime import timedelta
from models import db, User
from form import email_checker

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config["JWT_SECRET_KEY"] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(seconds=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600)))

jwt = JWTManager(app)
db.init_app(app)

blacklist = set()


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

        username = data.get("username")
        if db.session.query(User.username).filter(User.username == username).first():
            return jsonify({"status": "error", "message": "Username already in use"}), 400

        password = data.get("password")

        email = data.get("email")
        if db.session.query(User.email).filter(User.email == email).first():
            return jsonify({"status": "error", "message": "Email already in use"}), 400

        DateOfBirth = data.get("DateOfBirth")

        role = data.get("role")

        phone = data.get("phone")

        print("processed data:", username, password, email, DateOfBirth, phone, role, flush=True)

        if not all([username, password, email, DateOfBirth, phone, role]):
            return jsonify({"status": "error", "message": "Missing required fields"}), 400
        # Create a new User object
        new_user = User(username=username, password=password, email=email, DateOfBirth=DateOfBirth, phone=phone,
                        role=role)

        # Add the new User object to the session
        db.session.add(new_user)

        # Commit the session to save the changes to the database
        db.session.commit()

        return jsonify({"status": "success"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/login_user", methods=["GET"])
def login_user(data):
    try:
        username = data.get("username")
        password = data.get("password")
        if not all([username, password]):
            return jsonify({"status": "error", "message": "Missing required fields"}), 400
        user = db.session.query(User).filter(User.username == username).first()
        if not user:
            return jsonify({"status": "error", "message": "Username not found"}), 400
        if user.password != password:
            return jsonify({"status": "error", "message": "Username or Password incorrect"}), 400
        else:
            access_token = create_access_token(identity={'username': username})
            return jsonify({"status": "success", "access_token": access_token}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@jwt_required()
@app.route("/change_email", methods=["POST"])
def change_email(data):
    try:
        current_user = get_jwt_identity()['username']
        new_email = data.get('new_email')
        is_valid, message = email_checker(new_email)
        if not is_valid:
            return jsonify({"status": "error", "message": message}), 400

        user = db.session.query(User).filter(User.username == current_user).first()
        user.email = new_email
        db.session.commit()
        return jsonify({"status": "success", "message": "Email updated successfully"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@jwt_required()
@app.route("/change_account", methods=["POST"])
def change_password(data):
    current_user = get_jwt_identity()['username']
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    confirm_new_password = data.get('confirm_new_password')

    if not all([current_password, new_password, confirm_new_password]):
        return jsonify({"status": "error", "message": "All fields are required"}), 400

    if new_password != confirm_new_password:
        return jsonify({"status": "error", "message": "New passwords do not match"}), 400

    user = db.session.query(User).filter(User.username == current_user).first()

    if not user or user.password != current_password:
        return jsonify({"status": "error", "message": "Current password is incorrect"}), 400

    user.password = new_password
    db.session.commit()

    return jsonify({"status": "success", "message": "Password updated successfully"}), 200


@jwt_required()
@app.route("/delete_account", methods=["DELETE"])
def delete_account(data):
    try:
        current_user = get_jwt_identity()['username']
        user = db.session.query(User).filter(User.username == current_user).first()
        if user:
            db.session.delete(user)
            db.session.commit()
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


# Dictionary acting like switch statement for our different request handling functions
actions = {
    "register_user": register_user,
    "login_user": login_user,
    "logout": logout,
    "change_email": change_email,
    "change_password": change_password,
    "delete_account": delete_account,

}


@app.route("/api", methods=["POST", "GET"])
def api():
    # Pulls data from request
    data = request.json
    print("received data:", data, flush=True)
    # Action held within json file determines what action server performs
    action = data.get("action")

    # Calls functions
    if action in actions:
        return actions[action](data)
    else:
        return jsonify({'status': 'error', 'message': 'Invalid action'}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
