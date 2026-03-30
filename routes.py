from fastapi import APIRouter, HTTPException, Depends
from database import users_collection
from auth import hash_password, verify_password, create_token, decode_token
from models import UserCreate, UserLogin
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# 🔹 Register user
@router.post("/register")
def register(user: UserCreate):
    if users_collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="User already exists")

    user_doc = {
        "username": user.username,
        "password": hash_password(user.password),
        "role": user.role
    }
    users_collection.insert_one(user_doc)
    return {"msg": "User created successfully"}

# 🔹 Login user
@router.post("/login")
def login(user: UserLogin):
    db_user = users_collection.find_one({"username": user.username})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({
        "sub": db_user["username"],
        "role": db_user["role"]
    })
    return {"access_token": token, "token_type": "bearer"}

# 🔹 Get current user (protected)
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload

# 🔹 Protected route example
@router.get("/protected")
def protected_route(user=Depends(get_current_user)):
    return {"msg": "You are logged in!", "user": user}