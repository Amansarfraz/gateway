# auth_routes.py
from fastapi import APIRouter, HTTPException
from database import users_collection
from auth import hash_password, verify_password, create_access_token
from models.user import UserCreate, UserLogin

router = APIRouter(prefix="/auth", tags=["Auth"])

# 🔹 Register
@router.post("/register")
def register(user: UserCreate):
    if users_collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="User already exists")

    users_collection.insert_one({
        "username": user.username,
        "password": hash_password(user.password),
        "role": user.role
    })

    return {"msg": "User created"}

# 🔹 Login
@router.post("/login")
def login(user: UserLogin):
    db_user = users_collection.find_one({"username": user.username})

    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "sub": db_user["username"],
        "role": db_user["role"]
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }