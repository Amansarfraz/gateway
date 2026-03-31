# from datetime import datetime, timedelta
# from jose import jwt, JWTError
# from passlib.context import CryptContext

# SECRET_KEY = "CHANGE_THIS_SECRET_KEY"  # 🔥 Change this to a strong secret
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# # 🔹 Hash password
# def hash_password(password: str):
#     return pwd_context.hash(password)

# # 🔹 Verify password
# def verify_password(plain: str, hashed: str):
#     return pwd_context.verify(plain, hashed)

# # 🔹 Create JWT token
# def create_token(data: dict):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode.update({
#         "exp": expire,
#         "iat": datetime.utcnow()
#     })
#     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# # 🔹 Decode JWT token
# def decode_token(token: str):
#     try:
#         return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#     except JWTError:
#         return None
from fastapi import APIRouter, HTTPException
from database import users_collection
from auth import hash_password, verify_password, create_token
from models.user import UserCreate, UserLogin

router = APIRouter()

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

    token = create_token({
        "sub": db_user["username"],
        "role": db_user["role"]
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }