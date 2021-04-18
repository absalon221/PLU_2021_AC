from fastapi.testclient import TestClient
import pytest, hashlib, requests
from main import app

client = TestClient(app)

def test_auth():
    response = client.get(f"/auth?password=  &password_hash=16b7aa7f7e549ba129c776bb91ce1e692da103271242d44a9bc145cf338450c90132496ead2530f527b1bd7f50544f37e7d27a2d2bbb58099890aa320f40aca9")
    assert response.status_code == 401