from fastapi import FastAPI, Request, Response, Cookie, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse
from datetime import date
from pydantic import BaseModel
from hashlib import sha256
import secrets


app = FastAPI()
templates = Jinja2Templates(directory="templates")
security = HTTPBasic()

app.stored_login_session = []
app.stored_login_token = []
    
@app.get("/hello")
def print_date(request: Request, response: Response):
    return_date = date.today()
    #response.headers["content-type"] = "text/html"
    return templates.TemplateResponse("hello.html", {"request": request, "date": return_date})

@app.post("/login_session", status_code = 201)
def login_session(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "4dm1n")
    correct_password = secrets.compare_digest(credentials.password, "NotSoSecurePa$$")
    
    if not (correct_username and correct_password):
        raise HTTPException(status_code=401)
    
    session_token = sha256(f"{credentials.username}{credentials.password}".encode()).hexdigest()
    response.set_cookie(key="session_token", value=session_token)
    app.stored_login_session.append(session_token)
    
    if len(app.stored_login_session) > 5:
        app.stored_login_session.pop(0)
        

@app.post("/login_token", status_code = 201)
def login_token(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "4dm1n")
    correct_password = secrets.compare_digest(credentials.password, "NotSoSecurePa$$")
    
    if not (correct_username and correct_password):
        raise HTTPException(status_code=401)
    
    session_token = sha256(f"{credentials.username}{credentials.password}".encode()).hexdigest()
    response.set_cookie(key="value_token", value=session_token)
    app.stored_login_token.append(session_token)
    
    if len(app.stored_login_token) > 5:
        app.stored_login_token.pop(0)
    
    return {"token": session_token}

@app.get("/welcome_session", status_code=200)
def welcome_session(response: Response, session_token: str = Cookie(None), format: str = ""):
    if (session_token not in app.stored_login_session) or (session_token == ""):
        raise HTTPException(status_code=401, detail="Unathorised")
    
    if format == 'json':
        return {"message": "Welcome!"}
    elif format == 'html':
        return HTMLResponse(content="<h1>Welcome!</h1>")
    else:
        return PlainTextResponse(content="Welcome!")
        
@app.get("/welcome_token", status_code=200)
def welcome_token(response: Response, token: str, format: str = ""):
    if (token not in app.stored_login_token) or (token == ""):
        raise HTTPException(status_code=401, detail="Unathorised")
    
    if format == 'json':
        return {"message": "Welcome!"}
    elif format == 'html':
        return HTMLResponse(content="<h1>Welcome!</h1>")
    else:
        return PlainTextResponse(content="Welcome!")

@app.get("/logged_out", status_code=200)
def logged_out(response: Response, format: str = ""):
    if format == 'json':
        return {"message": "Logged out!"}
    elif format == 'html':
        return HTMLResponse(content="<h1>Logged out!</h1>")
    else:
        return PlainTextResponse(content="Logged out!")
    
@app.delete("/logout_session", status_code=302)
def logout_session(response: Response, session_token: str = Cookie(None), format: str = ""):
    if (session_token not in app.stored_login_session) or (session_token == ""):
        raise HTTPException(status_code=401, detail="Unathorised")
    
    app.stored_login_session.pop(app.stored_login_session.index(session_token))
    return RedirectResponse(url=f"/logged_out?format={format}")
    
    
@app.delete("/logout_token", status_code=302)
def logout_token(response: Response, token: str, format: str = ""):
    if (token not in app.stored_login_token) or (token == ""):
        raise HTTPException(status_code=401, detail="Unathorised")
    
    app.stored_login_token.pop(app.stored_login_token.index(token))
    return RedirectResponse(url=f"/logged_out?format={format}")