from fastapi.testclient import TestClient
import pytest, hashlib, requests
from main import app

client = TestClient(app)

def test_auth():
    response = client.get(f"/auth?password= &password_hash=78dfec637347c509fe8d78d55efbd28fa1666f146e3a964b7eda2551e6f36bf29b57266584fa47306ba7332e246e9d4406c5a72a9e609e2eca6e36a6ff505f36")
    assert response.status_code == 401