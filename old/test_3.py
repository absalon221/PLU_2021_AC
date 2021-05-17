from fastapi.testclient import TestClient
import pytest, requests
from main_3 import app
from requests.auth import HTTPBasicAuth

client = TestClient(app)

def test_logout_session_ok():
    login = "4dm1n"
    password = "NotSoSecurePa$$"
    # logowanie przez session
    #response = client.post("/login_session", auth=HTTPBasicAuth(login, password))
    # logowanie przez token
    response = client.post("/login_token", auth=HTTPBasicAuth(login, password))
    token_val = response.json()["token"]
       
    assert response.status_code == 201
    
    response = client.delete("/logout_session?format=json",
                             cookies = {"session_token": token_val})
    
    assert response.status_code == 302
    
def test_logout_session_notok():
    token_val = "B"
    response = client.delete("/logout_session?format=json",
                             cookies = {"session_token": token_val})
    
    assert response.status_code == 401
    
def test_logout_token_ok():
    login = "4dm1n"
    password = "NotSoSecurePa$$"
    # logowanie przez session
    response = client.post("/login_session", auth=HTTPBasicAuth(login, password))
    token_val = "A"
    # logownie przez token
    #response = client.post("/login_token", auth=HTTPBasicAuth(login, password))
    #token_val = response.json()["token"]
       
    assert response.status_code == 201
    
    response = client.delete(f"/logout_token?token={token_val}")
    
    assert response.status_code == 302

def test_logout_token_nieok():
    token_val = "B"
    response = client.delete(f"/logout_token?token={token_val}")
    
    assert response.status_code == 401
    
def test_sesja_token_sesja_token():
    login = "4dm1n"
    password = "NotSoSecurePa$$"
    
    response = client.post("/login_session", auth=HTTPBasicAuth(login, password))
    assert response.status_code == 201
    
    response = client.post("/login_token", auth=HTTPBasicAuth(login, password))
    token_val = "B" # response.json()["token"]
    assert response.status_code == 201
    
    response = client.delete("/logout_session?format=json")
    assert response.status_code == 302
    
    response = client.delete(f"/logout_token?token={token_val}")
    assert response.status_code == 401
    
def test_token_sesja_token_sesja():
    login = "4dm1n"
    password = "NotSoSecurePa$$"
    
    response = client.post("/login_token", auth=HTTPBasicAuth(login, password))
    token_val = response.json()["token"]
    assert response.status_code == 201
    
    response = client.post("/login_session", auth=HTTPBasicAuth(login, password))
    assert response.status_code == 201
    
    response = client.delete(f"/logout_token?token={token_val}")
    assert response.status_code == 302
    
    response = client.delete("/logout_session?format=json")
    assert response.status_code == 302