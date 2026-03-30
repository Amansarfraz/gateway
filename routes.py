from fastapi import APIRouter, Depends
from database import users_collection
from auth import hash_password, verify_password, create_token
from dependencies import get_current_user, role_required

router = APIRouter()

# Register
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
    return {"msg": "User created successfully"}

# Login (REAL JWT)
@router.post("/login")
def login(username: str, password: str):

    user = users_collection.find_one({"username": username})

    if not user or not verify_password(password, user["password"]):
        return {"error": "Invalid credentials"}

    token = create_token({
        "sub": user["username"],
        "role": user["role"]
    })

    return {"access_token": token}

# Protected route
@router.get("/protected")
def protected(user=Depends(get_current_user)):
    return {"msg": "You are authorized", "user": user}

# Admin only
@router.get("/admin")
def admin_only(user=Depends(role_required("admin"))):
    return {"msg": "Welcome Admin"}

# Owner example
@router.get("/owner")
def owner_only(user=Depends(role_required("owner"))):
    return {"msg": "Welcome Owner"}