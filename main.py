from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from datetime import date

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/hello")
def print_date(request: Request):
    return_date = date.today()
    return templates.TemplateResponse("hello.html", {"request": request, "date": return_date})