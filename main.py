from fastapi import FastAPI, Request, Response, Cookie, Depends
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from datetime import date
from pydantic import BaseModel
import base64, secrets
from hashlib import sha256

app = FastAPI()
templates = Jinja2Templates(directory="templates")
security = HTTPBasic()
#app.secret_key = "dfghjk54t576weufhuj"
#app.access_tokens = [0, 0]

class TokenResp(BaseModel):
    token: str
    
@app.get("/hello")
def print_date(request: Request, response: Response):
    return_date = date.today()
    response.headers["content-type"] = "text/html"
    return templates.TemplateResponse("hello.html", {"request": request, "date": return_date})

@app.post("/login_session")
def login_session(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "4dm1n")
    correct_password = secrets.compare_digest(credentials.password, "NotSoSecurePa$$")
    if not (correct_username and correct_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    #app.access_tokens[0]=1
    response.set_cookie(key="session_token", value=1)
    return
        

@app.post("/login_token")
def login_token(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "4dm1n")
    correct_password = secrets.compare_digest(credentials.password, "NotSoSecurePa$$")
    if not (correct_username and correct_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    #app.access_tokens[1]=2
    response.set_cookie(key="value_token", value=2)
    return TokenResp(token=2)