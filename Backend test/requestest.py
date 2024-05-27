import requests
def register():
    url = 'http://localhost:5001/api'
    data = {
        "action": "register_user",
        'username': "user1",
        'password': "password",
        'email': "blahblah@gmail.com",
        'DateOfBirth': "2000-01-01",
        'role': "user"
    }
    response = requests.post(url, json=data)
    if response.status_code == 201:
        print("Register success:", response.json())
    else:
        print("Register Fail:", response.json())

def login(password):
    url = 'http://localhost:5001/api'
    data = {
        "action": "login_user",
        'username': "user1",
        'password': password
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        token = response.json().get('access_token')
        print(f"Login successful, token: {token}")
        return token
    else:
        print("Login Fail:", response.json())
        return None

def logout(token):
    url = 'http://localhost:5001/api'
    headers = {'Authorization': f'Bearer {token}'}
    data = {
        "action": "logout"
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        print("Logout success:", response.json())
    else:
        print("Logout Fail:", response.json())

def change_password(token, current_password, new_password, confirm_new_password):
    url = 'http://localhost:5001/api'
    headers = {'Authorization': f'Bearer {token}'}
    data = {
        "action": "change_password",
        "current_password": current_password,
        "new_password": new_password,
        "confirm_new_password": confirm_new_password
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        print("Password changed successfully:", response.json())
    else:
        print("Failed to change password:", response.json())


def change_email(token, new_email):
    url = 'http://localhost:5001/api'
    headers = {'Authorization': f'Bearer {token}'}
    data = {
        "action": "change_email",
        "new_email": new_email
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        print("Email changed successfully:", response.json())
    else:
        print("Failed to change email:", response.json())





register()
token = login("password")
if token:
    change_password(token, "password", "NewPassword1!", "NewPassword1!")
    new_token = login("NewPassword1!")
    if new_token:
        print("Re-login successful with new password, new token:", new_token)
        change_email(new_token, "newemail@gmail.com")
        logout(new_token)
    else:
        print("Failed to log in with new password")
else:
    print("Initial login failed, cannot proceed with password change test.")
