# from fastapi import APIRouter, Depends
# from dependencies import role_required
# from database import db

# router = APIRouter(prefix="/admin", tags=["Admin"])

# students_collection = db["students"]

# # 🔥 Only admin can access
# @router.get("/students")
# def admin_students(user=Depends(role_required(["admin"]))):
#     return list(students_collection.find())
from fastapi import APIRouter, Depends
from dependencies import role_required
from database import students_collection

router = APIRouter(prefix="/admin", tags=["Admin"])

# 🔥 Only Admin
@router.get("/students")
def get_all_students(user=Depends(role_required(["admin"]))):
    data = list(students_collection.find())

    for d in data:
        d["_id"] = str(d["_id"])

    return data