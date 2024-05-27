import requests


def register():
    url = 'http://localhost:5001/api'
    data = {
        "action": "register_user",
        'username': "user2",
        'password': "password",
        'email': "blahblah@gmail.com",
        'DateOfBirth': "2000-01-01 00:00:00",
        'phone': "07722824206",
        'role': "user"
    }
    response = requests.post(url, json=data)
    if response.status_code == 201:
        print(response.json())
    else:
        print(response.json())


def login():
    url = 'http://localhost:5001/api'
    data = {
        "action": "login_user",
        'username': "user2",
        'password': "password"
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        token = response.json().get('access_token')
        print(f"Login successful, token: {token}")
        return token
    else:
        print(response.json())


def logout(token):
    url = 'http://localhost:5001/api'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        print(response.json())
    else:
        print(response.json())


register()
token = login()
if token:
    logout(token)
    new_token = login()
    if new_token:
        print("Re-login successful, new token obtained.")
