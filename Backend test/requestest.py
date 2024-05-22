import requests
def register():
    url = 'http://localhost:5001/api'
    data = {
        "action": "register_user",
        'username': "user1",
        'password': "password",
        'email': "blahblah@gmail.com",
        'DateOfBirth': "2000-01-01 00:00:00",
        'role': "user"
    }
    response = requests.post(url, json=data)
    if response.status_code == 201:
        print (response.json())
    else:
        print(response.json())

def login():
    url = 'http://localhost:5001/api'
    data = {
        "action": "login_user",
        'username': "user1",
        'password': "password"
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        token = response.json().get('access_token')
        print(f"Login successful, token: {token}")
        return token
    else:
        print(response.json())


register()