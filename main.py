from fastapi import FastAPI, Request, Response, Cookie
from fastapi.templating import Jinja2Templates
from datetime import date
import base64
from hashlib import sha256

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.secret_key = "dfghjk54t576weufhuj"
app.access_tokens = []

@app.get("/hello")
def print_date(request: Request, response: Response):
    return_date = date.today()
    response.headers["content-type"] = "text/html"
    return templates.TemplateResponse("hello.html", {"request": request, "date": return_date})

@app.post("/login_session")
def login_session(login: str, password: str, response: Response):
    to_check = login + ":" + password
    if to_check.encode() != "4dm1n:NotSoSecurePa$$":
        raise HTTPException(status_code=401)
    session_token = sha256(f"{login}{password}{app.secret_key}".encode()).hexdigest()
    app.access_tokens.append(session_token)
    response.set_cookie(key="session_token", value=session_token)
    return
        

@app.post("/login_token")
def login_token(*, response: Response, session_token: str = Cookie(None)):
    if session_token not in app.access_tokens:
        raise HTTPException(status_code=401, detail="Unathorised")
    else:
        return {"token": session_token}