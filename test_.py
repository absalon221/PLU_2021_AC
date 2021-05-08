from fastapi.testclient import TestClient
import pytest, aiosqlite
from main import app

#client = TestClient(app)

def test_categories():
    with TestClient(app) as client:
        response = client.get("/categories")
    
        assert response.status_code == 200
        assert response.json() == {"Categories": [{"id": 1, "name": "Beverages"},
                                              {"id": 2, "name": "Condiments"},
                                              {"id": 3, "name": "Confections"},
                                              {"id": 4, "name": "Dairy Products"},
                                              {"id": 5, "name": "Grains/Cereals"},
                                              {"id": 6, "name": "Meat/Poultry"},
                                              {"id": 7, "name": "Produce"},
                                              {"id": 8, "name": "Seafood"}]}