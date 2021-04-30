from fastapi.testclient import TestClient
import pytest
from main import app

client = TestClient(app)

def test_login_session():
    login = "4dm1n"
    password = "NotSoSecurePa$$"
    response = client.post(f"/login_session?login={login}&password={password}")
    
    assert response == "OK"
    