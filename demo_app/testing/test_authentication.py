import json
import os
from dotenv import load_dotenv

load_dotenv()
#
# """
# Below are Registration Test Cases;
# +ve Test Cases : Return --> Json Response                        - 1 Nos
# -ve Test Cases : Raises --> HTTP Exception Error Messages        - 4 Nos
#
# test_registration_success_200: Successful User Registration      : 200
# test_registration_email_exists_409: Email-ID Already Exists      : 409
# test_registration_invalid_email_401: Invalid Email-ID Format     : 401
# test_registration_password_mismatch_401: Password Mismatch Error : 401
# test_registration_password_format_401: Incorrect Password Format : 401
# """
# """++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"""
#
#
def test_registration_success_200(client):
    data = {
        "username": os.environ.get('username'),
        "email": os.environ.get('email'),
        "password": os.environ.get('password'),
        "confirm_password": os.environ.get('confirm_password')
    }
    response = client.post('/register', json.dumps(data))
    assert response.status_code == 200
    assert response.json()['message'] == 'User Registered Successfully'


def test_registration_email_exists_409(client):
    data = {
        "username": os.environ.get('username'),
        "email": os.environ.get('email'),
        "password": os.environ.get('password'),
        "confirm_password": os.environ.get('confirm_password')
    }
    response = client.post('/register', json.dumps(data))
    assert response.status_code == 409
    assert "Email Already Exists"
#
#
def test_registration_invalid_email_401(client):
    data = {
        "username": os.environ.get('username'),
        "email": "Invalid-Email-Format",
        "password": os.environ.get('password'),
        "confirm_password": os.environ.get('confirm_password')
    }
    response = client.post('/register', json.dumps(data))
    assert response.status_code == 401
    # assert "Invalid Email-ID Format"


def test_registration_password_mismatch_401(client):
    data = {
        "username": "TestUserSample",
        "email": "TestUserSample@gmail.com",
        "password": "TestUser@12345",
        "confirm_password": "TestUser@1234"
    }
    response = client.post('/register', json.dumps(data))
    assert response.status_code == 401
    assert "Password Does Not Match"


def test_registration_password_format_401(client):
    data = {
        "username": "TestUserSample",
        "email": "TestUserSample@gmail.com",
        "password": 'password',
        "confirm_password": 'password'
    }
    response = client.post('/register', json.dumps(data))
    assert response.status_code == 401
    assert "Invalid Password Format."


"""++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"""
"""
Below are Login Test Cases;
+ve Test Cases : Return --> Json Response                        - 1 Nos
-ve Test Cases : Raises --> HTTP Exception Error Messages        - 2 Nos

test_login_success_200: Successful User Login                    : 200
test_login_incorrect_credentials_404: Incorrect Credentials      : 404
test_login_incorrect_password_404: Incorrect Password            : 404
"""


def test_login_success_200(client):
    data = {
        "username": os.environ.get('email'),
        "password": os.environ.get('password'),
    }
    response = client.post('/login', json.dumps(data))
    assert response.status_code == 200
    assert "access_token: {}, refresh_token: {}, token_type: bearer"


def test_login_incorrect_credentials_404(client):
    data = {
        "username": "unknown@user.in",
        "password": "UnknownUser@1234"
    }
    response = client.post('/login', json.dumps(data))
    assert response.status_code == 404
    assert "User Not Found"


def test_login_incorrect_password_404(client):
    data = {
        "username": os.environ.get('email'),
        "password": "User@12345"
    }
    response = client.post('/login', json.dumps(data))
    assert response.status_code == 404
    assert "Incorrect Password! Please Try Again"


"""++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"""

def test_all_users_200(client):
    response = client.get('/get_user')
    assert response.status_code == 200
    assert "Users Fetched Successfully"
