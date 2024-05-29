import requests


def register():
    url = 'http://localhost:5001/api'
    data = {
        "action": "register_user",
        'username': "user2",
        'password': "password",
        'email': "blahblah@gmail.com",
        'DateOfBirth': "14/04/2004",
        'phone': "07722824206",
        'role': "admin"
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
    data = {
        "action": "logout"
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print(response.json())
    else:
        print(response.json())

def delete_account(token):
    url = 'http://localhost:5001/api'
    headers = {'Authorization': f'Bearer {token}'}
    data = {
        "action": "admin_delete_account",
        'delete_username': "user1"
    }
    print(headers,data)
    response = requests.post(url, headers=headers, json=data)
    print(response.json())

def view_users(token):
    url = 'http://localhost:5001/api'
    headers = {'Authorization': f'Bearer {token}'}
    data = {
        "action": "view_users",
    }
    response = requests.post(url, headers=headers, json=data)
    print(response.json())

register()
token = login()
#delete_account(token)
view_users(token)

#if token:
 #   logout(token)
  #  new_token = login()
   # if new_token:
    #    print("Re-login successful, new token obtained.")
