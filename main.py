from fastapi import FastAPI, Response, status
import hashlib

app = FastAPI()
    
@app.get('/auth', status_code = 401)
def auth(password:str, password_hash:str, response:Response):
    if (password != None) and (password_hash != None) and (password.isspace() == False) and (password_hash.isspace() == False):
        calculated_hash = str(hashlib.sha512(bytes(password, encoding='utf-8')).hexdigest())
        if password_hash == calculated_hash:
            response.status_code = 204