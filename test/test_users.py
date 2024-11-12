
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import schemas

from jose import jwt
from app.config import settings
    



# def test_root(client):
#     res = client.get("/")
#     print(res.json().get('message'))
#     assert res.json().get('message') == 'Hello world erm hi !!'
#     assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users/", json={"email": "helo123@gmail.com", "password": "password123"})
    
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "helo123@gmail.com"
    assert res.status_code == 201

def test_login_user(client, test_user):
    res = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, 
                         settings.secret_key, algorithms= [settings.algorithm] )
    id = payload.get('user_id')
    assert id == test_user['id']
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 403),
    ('sanjeev@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    ( None , 'password123', 422),
    ('sanjeev@gmail.com', None, 422)
])
def test_incorrect_login( test_user, client, email, password, status_code):
    #print(f"Testing login with email: {email}, password: {password}")
    res = client.post(
        "/login", data={"username": email, "password": password})
    
    # print(f"Response status code: {res.status_code}")
    # print(f"Response content: {res.json()}")
    assert res.status_code == status_code
    assert res.json().get('detail') == 'Invalid Credentials'
#doesn't work completely problem with the form data encoding
#When you use client.post("/login", data={"username": email, "password":password}), 
# the data dictionary is converted into a form-encoded request. If you pass None in
#  the dictionary as part of the request data, the Starlette or FastAPI TestClient 
# may convert it to a string "None" when encoding the form data.

#ignore for now moving on

