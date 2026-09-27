from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import os

app = FastAPI(title="Employee Management API", version="1.0.0")
security = HTTPBearer()
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("JWT_SECRET", "change-this-secret")
ALGORITHM = "HS256"

users = {}
employees = {}
next_employee_id = 1

class Register(BaseModel):
    username: str
    password: str

class Login(BaseModel):
    username: str
    password: str

class Employee(BaseModel):
    name: str
    email: EmailStr
    department: str
    designation: str

def token_for(username):
    return jwt.encode(
        {"sub": username, "exp": datetime.now(timezone.utc) + timedelta(hours=2)},
        SECRET_KEY, algorithm=ALGORITHM
    )

def current_user(creds: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(creds.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username or username not in users:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/")
def root():
    return {"message": "Employee Management API", "version": app.version}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/ready")
def ready():
    return {"status": "ready"}

@app.post("/auth/register", status_code=201)
def register(data: Register):
    if data.username in users:
        raise HTTPException(status_code=409, detail="User already exists")
    users[data.username] = pwd.hash(data.password)
    return {"message": "Registration successful"}

@app.post("/auth/login")
def login(data: Login):
    if data.username not in users or not pwd.verify(data.password, users[data.username]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": token_for(data.username), "token_type": "bearer"}

@app.post("/employees", status_code=201)
def create_employee(data: Employee, _: str = Depends(current_user)):
    global next_employee_id
    item = {"id": next_employee_id, **data.model_dump()}
    employees[next_employee_id] = item
    next_employee_id += 1
    return item

@app.get("/employees")
def list_employees(_: str = Depends(current_user)):
    return list(employees.values())

@app.get("/employees/{employee_id}")
def get_employee(employee_id: int, _: str = Depends(current_user)):
    if employee_id not in employees:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employees[employee_id]

@app.put("/employees/{employee_id}")
def update_employee(employee_id: int, data: Employee, _: str = Depends(current_user)):
    if employee_id not in employees:
        raise HTTPException(status_code=404, detail="Employee not found")
    employees[employee_id] = {"id": employee_id, **data.model_dump()}
    return employees[employee_id]

@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int, _: str = Depends(current_user)):
    if employee_id not in employees:
        raise HTTPException(status_code=404, detail="Employee not found")
    del employees[employee_id]
    return {"message": "Employee deleted"}
