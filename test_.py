from fastapi.testclient import TestClient
import pytest, aiosqlite
from main import app

#client = TestClient(app)

def test_categories():
    with TestClient(app) as client:
        response = client.get("/categories")
    
        assert response.status_code == 200
        assert response.json() == {"categories": [{"id": 1, "name": "Beverages"},
                                              {"id": 2, "name": "Condiments"},
                                              {"id": 3, "name": "Confections"},
                                              {"id": 4, "name": "Dairy Products"},
                                              {"id": 5, "name": "Grains/Cereals"},
                                              {"id": 6, "name": "Meat/Poultry"},
                                              {"id": 7, "name": "Produce"},
                                              {"id": 8, "name": "Seafood"}]}
        
def test_customers():
    with TestClient(app) as client:
        response = client.get("/customers")
    
        assert response.status_code == 200
        print(response.json())
        
def test_products():
    with TestClient(app) as client:
        response = client.get("/products/0")
        
        #assert response.json() == {"id": 1, "name": "Chai"}
        assert response.status_code == 404
        
def test_employees():
    with TestClient(app) as client:
        response = client.get("/employees?offset=2")
        
        assert response.status_code == 400
        #assert response.json() == {"employees": [{"id":1,"last_name":"Davolio","first_name":"Nancy","city":"Seattle"},
        #                                         {"id":2,"last_name":"Fuller","first_name":"Andrew","city":"Tacoma"},
        #                                         {"id":3,"last_name":"Leverling","first_name":"Janet","city":"Kirkland"},
        #                                         {"id":4,"last_name":"Peacock","first_name":"Margaret","city":"Redmond"},
        #                                         {"id":5,"last_name":"Buchanan","first_name":"Steven","city":"London"},
        #                                         {"id":6,"last_name":"Suyama","first_name":"Michael","city":"London"},
        #                                         {"id":7,"last_name":"King","first_name":"Robert","city":"London"},
        #                                         {"id":8,"last_name":"Callahan","first_name":"Laura","city":"Seattle"},
        #                                         {"id":9,"last_name":"Dodsworth","first_name":"Anne","city":"London"},]}
        
def test_product_order():
    with TestClient(app) as client:
        response = client.get("/products/0/orders")
        assert response.status_code == 404
        
        response = client.get("/products/1/orders")
        assert response.status_code == 200
        
        response = client.get("/products/11/orders")
        assert response.json() == {"orders": [{"id": "10248", "customer": "Vins et alcools Chevalier", "quantity": "12", "total_price": "{:.2f}".format((14*12)-(0*(14*12)))}]}
        
def test_add_category():
    with TestClient(app) as client:
        response = client.post("/categories", json = {"name": "test category"})
        assert response.status_code == 201
        
def test_modify_category():
    with TestClient(app) as client:
        response = client.post("/categories", json = {"name": "test category"})
        assert response.status_code == 201
        assert response.json() == {"id": 9, "name": "test category"}
        
        response = client.put("/categories/9", json = {"name": "BLUBOR"})
        assert response.status_code == 200
        assert response.json() == {"id": 9, "name": "BLUBOR"}      
        
        response = client.delete("/categories/9")
        assert response.status_code == 200
        assert response.json() == {"deleted": 1}
        
        response = client.put("/categories/5846", json = {"name": "BLUBOR"})
        assert response.status_code == 404
        
        response = client.delete("/categories/5846")
        assert response.status_code == 404