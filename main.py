from fastapi import FastAPI, Request, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List, Dict
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded

# ✅ Correct imports based on your structure
from auth import create_access_token, hash_password, verify_password, get_current_user
from database import users_collection  # remove appointments_collection

from routes import auth_routes, student_routes, admin_routes

# -----------------------------
# FastAPI App
# -----------------------------
app = FastAPI(title="College API with JWT & Rate Limiter", version="1.0.0")

# -----------------------------
# Rate Limiter Setup
# -----------------------------
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(status_code=429, content={"error": "Too many requests"})

# -----------------------------
# Models
# -----------------------------
class UserRegister(BaseModel):
    username: str
    password: str
    role: str  # "admin" or "student"

class Student(BaseModel):
    name: str
    age: int
    course: str

# -----------------------------
# Root & Health
# -----------------------------
@app.get("/")
@limiter.limit("5/minute")
def root(request: Request):
    return {"message": "College API Running 🚀"}

@app.get("/health")
def health_check():
    return {"status": "OK"}

# -----------------------------
# User Registration
# -----------------------------
@app.post("/register")
def register_user(user: UserRegister):
    existing = users_collection.find_one({"username": user.username})
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")
    if user.role not in ["admin", "student"]:
        raise HTTPException(status_code=400, detail="Role must be 'admin' or 'student'")

    hashed_pw = hash_password(user.password)
    users_collection.insert_one({
        "username": user.username,
        "password": hashed_pw,
        "role": user.role
    })
    return {"message": f"User {user.username} registered successfully ✅"}

# -----------------------------
# Login & Generate JWT
# -----------------------------
@app.post("/login")  # ✅ Renamed to /login for consistency with your old code
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_collection.find_one({"username": form_data.username})
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    token_data = {"sub": form_data.username, "role": user["role"]}
    access_token = create_access_token(token_data)
    return {"access_token": access_token, "token_type": "bearer"}

# -----------------------------
# Protected Route Example
# -----------------------------
@app.get("/protected")
def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": "Access granted ✅", "user": current_user}

# -----------------------------
# Students Management
# -----------------------------
@app.get("/students")
def get_students(current_user: dict = Depends(get_current_user)):
    """
    Admins see all students, students see only their own records
    """
    if current_user["role"] == "student":
        students = list(appointments_collection.find({"owner": current_user["username"]}, {"_id": 0}))
    else:
        students = list(appointments_collection.find({}, {"_id": 0}))
    return students

@app.post("/students")
def create_student(student: Student, current_user: dict = Depends(get_current_user)):
    student_dict = student.dict()
    student_dict["owner"] = current_user["username"]

    result = appointments_collection.insert_one(student_dict)
    student_dict["_id"] = str(result.inserted_id)

    return {
        "message": "Student created successfully ✅",
        "data": student_dict
    }

# -----------------------------
# Include Existing Routers
# -----------------------------
app.include_router(auth_routes.router)
app.include_router(student_routes.router)
app.include_router(admin_routes.router)
