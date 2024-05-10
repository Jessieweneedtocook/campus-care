from flask import Flask, request, jsonify
from flask_mysqldb import MySQL


app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'team37'
app.config['MYSQL_DATABASE_DB'] = 'campus_care'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql = MySQL(app)

@app.route('/users', methods=['POST'])
def add_user():
    cur = mysql.get_db().cursor()
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']
    dob = request.json['dob']
    role = request.json.get('role', 'User')
    cur.execute("INSERT INTO Users (Username, Password, Email, DateOfBirth, Role) VALUES (%s, %s, %s, %s, %s)", (username, password, email, dob, role))
    mysql.get_db().commit()
    cur.close()
    return jsonify({'message': 'User added successfully'})

if __name__ == '__main__':
    app.run(debug=True)
