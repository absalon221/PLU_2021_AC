from fastapi.testclient import TestClient
import pytest
from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello world!"}

@pytest.mark.parametrize("name", ["Zenek", "Marek", "Alojzy Niezdąży"])
def test_hello_name(name):
    response = client.get(f"/hello/{name}")
    assert response.status_code == 200
    assert response.text == f'"Hello {name}"'

def test_counter():
    response = client.get(f"/counter")
    assert response.status_code == 200
    assert response.text == '"1"'
    # 2nd Try
    response = client.get(f"/counter")
    assert response.status_code == 200
    assert response.text == '"2"'
    
def test_method():
    response = client.post(f"/method")
    assert response.status_code == 201  
    assert response.json() == {"method": "POST"}