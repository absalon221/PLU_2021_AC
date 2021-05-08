import sqlite3
from fastapi import Cookie, FastAPI, HTTPException, Query, Request, Response
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List

app = FastAPI()


@app.on_event("startup")
async def startup():
    app.db_connection = sqlite3.connect("northwind.db")
    app.db_connection.text_factory = lambda b: b.decode(errors="ignore")  # northwind specific


@app.on_event("shutdown")
async def shutdown():
    app.db_connection.close()
    
@app.get("/")
def hello(status_code=200):
    return
    
@app.get("/categories", status_code=200)
async def categories():
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute("SELECT CategoryID, CategoryName FROM Categories ORDER BY CategoryID").fetchall()
    return {"categories": [{"id": x['CategoryID'], "name": x['CategoryName']} for x in data]}

@app.get("/customers", status_code=200)
async def customers():
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute("SELECT CustomerID, CompanyName, Address, City, PostalCode, Country FROM Customers ORDER BY CustomerID").fetchall()
    return {"customers": [{"id": x['CustomerID'], "name": x['CompanyName'], "full_adress": f"{x['Address']} {x['PostalCode']} {x['City']} {x['Country']}"} for x in data]}