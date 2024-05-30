from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from datetime import timedelta
from extensions import db, jwt
from Auth import auth_bp, auth_actions
from User import user_bp, user_actions
from Admin import admin_bp, admin_actions


load_dotenv()

app = Flask(__name__)
CORS(app)

#config data
app.config["JWT_SECRET_KEY"] = os.getenv('SECRET_KEY')
app.config['JWT_ALGORITHM'] = os.getenv('JWT_ALGORITHM')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(seconds=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600)))

#Initialises db and jwt
db.init_app(app)
jwt.init_app(app)

#Pulls blueprints from other files
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(admin_bp, url_prefix='/admin')

# Dictionary acting like switch statement for our different request handling functions, combines func dicts from other files
actions = {**auth_actions, **user_actions, **admin_actions}


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
