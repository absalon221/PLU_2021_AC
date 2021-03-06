from fastapi import FastAPI, Response, status
from pydantic import BaseModel
import hashlib, datetime

class Patient_input(BaseModel):
    name: str
    surname: str

class Patient_processed(BaseModel):
    id: int
    name: str
    surname: str
    register_date: str
    vaccination_date: str

app = FastAPI()
app.counter = 0
patients_dict = {}
    
@app.get('/auth', status_code = 401)
def auth(password:str, password_hash:str, response:Response):
    if (password != None) and (password_hash != None) and (password != "") and (password_hash != "") and (password.isspace() == False) and (password_hash.isspace() == False):
        calculated_hash = str(hashlib.sha512(bytes(password, encoding='utf-8')).hexdigest())
        if password_hash == calculated_hash:
            response.status_code = 204
            
@app.post('/register', status_code = 201, response_model=Patient_processed)
def register(patient: Patient_input):
    app.counter += 1
    reg_date = datetime.date.today()
    vacc_date = reg_date + datetime.timedelta(days = (sum(map(str.isalpha, patient.name)) + sum(map(str.isalpha, patient.surname))))
    
    patient_data = Patient_processed(id=int(app.counter), name=patient.name.title(), surname=patient.surname.title(), register_date=str(reg_date),  vaccination_date=str(vacc_date))
    patients_dict.update({app.counter: patient_data})
    
    return patient_data

@app.get('/patient/{id}', status_code=404, response_model=Patient_processed)
def is_patient_known(id: int, response: Response):
    if(id < 1):
        response.status_code = 400
        return
    if(id <= app.counter):
        response.status_code = 200
        read_patient_data = patients_dict.get(id)
        return read_patient_data

    