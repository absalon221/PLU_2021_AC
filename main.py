import sqlite3
from fastapi import Cookie, FastAPI, HTTPException, Query, Request, Response
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List

app = FastAPI()

#######

@app.on_event("startup")
async def startup():
    app.db_connection = sqlite3.connect("northwind.db")
    app.db_connection.text_factory = lambda b: b.decode(errors="ignore")  # northwind specific

@app.on_event("shutdown")
async def shutdown():
    app.db_connection.close()
    
#######
    
### ZADANIE 4.1  ###

@app.get("/categories", status_code=200)
async def categories():
    app.db_connection.row_factory = sqlite3.Row # umożliwia indeksowanie po nagłówkach kolumn
    data = app.db_connection.execute("SELECT CategoryID, CategoryName FROM Categories ORDER BY CategoryID").fetchall()
    return {"categories": [{"id": x['CategoryID'], "name": x['CategoryName']} for x in data]}

@app.get("/customers", status_code=200)
async def customers():
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute("SELECT CustomerID, CompanyName, Address || ' ' || PostalCode || ' ' || City || ' ' || Country AS FullAddress FROM Customers ORDER BY CustomerID").fetchall() # skleja kolumny adresu w taką, jaką chcemy
    return {"customers": [{"id": x['CustomerID'], "name": x['CompanyName'], "full_address": x['FullAddress']} for x in data]}

### ZADANIE 4.2 ###

@app.get("/products/{id}", status_code=200)
async def products(id: int):
    app.db_connection.row_factory = sqlite3.Row
    products = app.db_connection.execute(f"SELECT ProductID, ProductName FROM Products WHERE ProductID = {id}").fetchone()
    
    if products: 
        return {"id": products['ProductID'], "name": products['ProductName']}
    raise HTTPException(status_code=404)   
    