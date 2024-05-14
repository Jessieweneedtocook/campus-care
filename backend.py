from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

def get_db_connection():
    db = mysql.connector.connect(host='localhost', user='root', password='team37', port=32001)
    return db

def execute_query(query, data=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if data:
        cursor.execute(query, data)
    else:
        cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()
def register_user(data):
    try:
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

actions = {
    "register_user": register_user,
    "login_user": login_user
}
@app.route("/api", methods=["POST","GET"])
def api():
    data = request.json
    action = data.get("action")

    if action in actions:
        return actions[action](data)
    else:
        return jsonify({'status': 'error', 'message': 'Invalid action'}), 400



@app.route("/")
def hello_world():
    return render_template("")