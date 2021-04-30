from fastapi import FastAPI, Request, Response, Cookie, Depends
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from datetime import date
from pydantic import BaseModel
from hashlib import sha256
import secrets


app = FastAPI()
templates = Jinja2Templates(directory="templates")
security = HTTPBasic()

app.stored_login_session = ""
app.stored_login_token = ""
    
@app.get("/hello")
def print_date(request: Request, response: Response):
    return_date = date.today()
    response.headers["content-type"] = "text/html"
    return templates.TemplateResponse("hello.html", {"request": request, "date": return_date})

@app.post("/login_session", status_code = 201)
def login_session(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "4dm1n")
    correct_password = secrets.compare_digest(credentials.password, "NotSoSecurePa$$")
    
    if not (correct_username and correct_password):
        raise HTTPException(status_code=401)
    
    session_token = sha256(f"{credentials.username}{credentials.password}".encode()).hexdigest()
    response.set_cookie(key="session_token", value=session_token)
    app.stored_login_session = session_token
        

@app.post("/login_token", status_code = 201)
def login_token(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "4dm1n")
    correct_password = secrets.compare_digest(credentials.password, "NotSoSecurePa$$")
    
    if not (correct_username and correct_password):
        raise HTTPException(status_code=401)
    
    session_token = sha256(f"{credentials.username}{credentials.password}".encode()).hexdigest()
    response.set_cookie(key="value_token", value=session_token)
    app.stored_login_token = session_token
    return {"token": session_token}