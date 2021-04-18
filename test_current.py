from fastapi.testclient import TestClient
import pytest, hashlib, requests
from main import app

client = TestClient(app)

def test_auth():
    response = client.get(f"/auth?password=&password_hash=16b7aa7f7e549ba129c776bb91ce1e692da103271242d44a9bc145cf338450c90132496ead2530f527b1bd7f50544f37e7d27a2d2bbb58099890aa320f40aca9")
    assert response.status_code == 401
    
def test_register():
    # 1
    response = client.post(f"/register", json={"name": "Jan", "surname": "Nowak"})
    assert response.status_code == 201
    assert response.json() == {"id": 1,"name": "Jan","surname": "Nowak", "register_date": "2021-04-18",  "vaccination_date": "2021-04-26"}
    # 2
    response = client.post(f"/register", json={"name": "Blob", "surname": "Blaab"})
    assert response.status_code == 201
    assert response.json() == {"id": 2,"name": "Blob","surname": "Blaab", "register_date": "2021-04-18",  "vaccination_date": "2021-04-27"}
    # test memory
    # 1
    response = client.get(f"/patient/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1,"name": "Jan","surname": "Nowak", "register_date": "2021-04-18",  "vaccination_date": "2021-04-26"}
    # 2
    response = client.get(f"/patient/0")
    assert response.status_code == 400
    # 3
    response = client.get(f"/patient/5")
    assert response.status_code == 404