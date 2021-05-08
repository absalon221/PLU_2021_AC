import aiosqlite, sqlite3
from fastapi import FastAPI

app = FastAPI()


@app.on_event("startup")
async def startup():
    app.db_connection = await aiosqlite.connect("northwind.db")
    app.db_connection.text_factory = lambda b: b.decode(errors="ignore")  # northwind specific


@app.on_event("shutdown")
async def shutdown():
    await app.db_connection.close()
    
@app.get("/")
def hello(status_code=200):
    return
    
@app.get("/categories", status_code=200)
async def categories():
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute("SELECT DategoryID, CategoryName FROM Categories ORDER BY CategoryID").fetchall()
    return {"categories": [{"id": x['CategoryID'], "name": x['CategoryName']} for x in data]}

#@app.get("/customers")