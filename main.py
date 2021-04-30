from fastapi import FastAPI, Request, Response, Cookie, Depends
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from datetime import date
import base64
from hashlib import sha256

app = FastAPI()
templates = Jinja2Templates(directory="templates")
security = HTTPBasic()
#app.secret_key = "dfghjk54t576weufhuj"
app.access_tokens = [0, 0]

@app.get("/hello")
def print_date(request: Request, response: Response):
    return_date = date.today()
    response.headers["content-type"] = "text/html"
    return templates.TemplateResponse("hello.html", {"request": request, "date": return_date})

@app.post("/login_session")
def login_session(credentials: HTTPBasicCredentials = Depends(security)):
    if not (credentials.username == "4dm1n") or not (credentials.password == "NotSoSecurePa$$"):
        raise HTTPException(status_code=401)
    #session_token = sha256(f"{credentials.username}{credentials.password}{app.secret_key}".encode()).hexdigest()
    #app.access_tokens.append(session_token)
    app.access_tokens[0]=1
    response.set_cookie(key="session_token", value=1)
    return
        

@app.post("/login_token")
def login_token(credentials: HTTPBasicCredentials = Depends(security)):
    if not (credentials.username == "4dm1n") or not (credentials.password == "NotSoSecurePa$$"):
        raise HTTPException(status_code=401)
    app.access_tokens[1]=2
    return {"token": 2}