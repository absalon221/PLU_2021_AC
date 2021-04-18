from fastapi import FastAPI, Response, status
from pydantic import BaseModel
import hashlib, datetime

app = FastAPI()
app.counter = 0
    
@app.get('/auth', status_code = 401)
def auth(password:str, password_hash:str, response:Response):
    if (password != None) and (password_hash != None) and (password != "") and (password_hash != "") and (password.isspace() == False) and (password_hash.isspace() == False):
        calculated_hash = str(hashlib.sha512(bytes(password, encoding='utf-8')).hexdigest())
        if password_hash == calculated_hash:
            response.status_code = 204
            
@app.post('/register', status_code = 201)
def register(name:str, surname:str):
    app.counter += 1
    register_date = datetime.date.today()
    vaccination_date = register_date + datetime.timedelta(days = (len(name) + len(surname)))
   
    return {"id": str(app.counter),"name": name,"surname": surname, "register_date": str(register_date),  "vaccination_date":str(vaccination_date)}