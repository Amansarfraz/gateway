from fastapi import APIRouter, Depends, Request
from database import users_collection
from auth import hash_password, verify_password, create_token
from dependencies import get_current_user, role_required

router = APIRouter()

# 🔹 Register
@router.post("/register")
def register(username: str, password: str, role: str = "user"):

    if users_collection.find_one({"username": username}):
        return {"error": "User already exists"}

    user = {
        "username": username,
        "password": hash_password(password),
        "role": role
    }

    users_collection.insert_one(user)

    return {"msg": "User created"}


from models import UserLogin

@router.post("/login")
def login(user: UserLogin):   # ✅ Pydantic model
    db_user = users_collection.find_one({"username": user.username})

    if not db_user or not verify_password(user.password, db_user["password"]):
        return {"error": "Invalid credentials"}

    token = create_token({
        "sub": db_user["username"],
        "role": db_user["role"]
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }
# 🔐 🔹 Protected (ALL logged users)
@router.get("/protected")
def protected(user=Depends(get_current_user)):
    return {
        "msg": "You are logged in",
        "user": user
    }


# 🔥 🔹 Admin ONLY (FULL ACCESS)
@router.get("/admin")
def admin_only(user=Depends(role_required(["admin"]))):
    return {"msg": "Welcome Admin 👑 (Full Access)"}


# 🔥 🔹 User + Admin Access
@router.get("/user")
def user_access(user=Depends(role_required(["user", "admin"]))):
    return {"msg": "User Access Allowed 👍"}


# 🔥 🔹 Owner Example (Optional)
@router.get("/owner")
def owner_only(user=Depends(role_required(["owner", "admin"]))):
    return {"msg": "Owner Access"}