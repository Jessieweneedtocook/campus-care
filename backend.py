from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

def get_db_connection():
    #Makes connection to database when needed
    db = mysql.connector.connect(host='localhost', user='root', password='team37', port=32001)
    return db

def execute_query(query, data=None):
    #Code for executing queries
    conn = get_db_connection()
    cursor = conn.cursor()
    #If statement allows for queries whether inputting data or not
    if data:
        cursor.execute(query, data)
    else:
        cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()
def register_user(data):
    try:
        #Gonna need to add some verification to ensure no overlapping usernames/ emails
        username = data.get("username")
        password = data.get("password")
        email = data.get("email")
        DateOfBirth = data.get("DateofBirth")
        role = data.get("role")
        query = "INSERT INTO Users (Username, Password, Email, DateOfBirth, Role) VALUES (%s, %s, %s, %s, %s)"
        execute_query(query, (username, password, email, DateOfBirth, role))
        return jsonify({"status": "success"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def login_user(data):
    try:
        username = data.get("username")
        password = data.get("password")

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def change_email(data):

def change_password(data):

def delete_account(data):


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
    #Action held within json file determines what action server performs
    action = data.get("action")

    #Calls functions
    if action in actions:
        return actions[action](data)
    else:
        return jsonify({'status': 'error', 'message': 'Invalid action'}), 400



@app.route("/")
def hello_world():
    return render_template("")