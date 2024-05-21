from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os
from dotenv import load_dotenv
from models import db, User

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config["JWT_SECRET_KEY"] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

jwt = JWTManager(app)
db.init_app(app)

#from users.views import users_blueprint
#from admin.views import admin_blueprint

#app.register_blueprint(users_blueprint)
#app.register_blueprint(admin_blueprint)

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

        print("processed data:",username, password, email, DateOfBirth, role,flush=True)
        if not all([username, password, email, DateOfBirth, role]):
            return jsonify({"status": "error", "message": "Missing required fields"}), 400
        # Create a new User object
        new_user = User(username=username, password=password, email=email, DateOfBirth=DateOfBirth, role=role)

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
        user = db.session.query(User).filter(User.username == username).one()
        if not user:
            return jsonify({"status": "error", "message": "Username not found"}), 400
        if user.password != password:
            return jsonify({"status": "error", "message": "Username or Password incorrect"}), 400
        else:
            access_token = create_access_token(identity={'username': username})
            return jsonify(access_token=access_token), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@jwt_required()
@app.route("/change_email", methods=["POST"])
def change_email(data):
    pass
    return
@jwt_required()
@app.route("/change_account", methods=["POST"])
def change_password(data):
    pass
    return
@jwt_required()
@app.route("/delete_account", methods=["POST"])
def delete_account(data):
    pass
    return

#Dictionary acting like switch statement for our different request handling functions
actions = {
    "register_user": register_user,
    "login_user": login_user,
    "change_email":change_email,
    "change_password": change_password,
    "delete_account": delete_account,


}
@app.route("/api", methods=["POST","GET"])
def api():
    #Pulls data from request
    data = request.json
    print ("received data:",data, flush=True)
    #Action held within json file determines what action server performs
    action = data.get("action")

    #Calls functions
    if action in actions:
        return actions[action](data)
    else:
        return jsonify({'status': 'error', 'message': 'Invalid action'}), 400



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

