# from fastapi import APIRouter, Depends
# from database import db
# from dependencies import get_current_user

# router = APIRouter(prefix="/students", tags=["Students"])

# students_collection = db["students"]

# # 🔹 Add Student
# @router.post("/")
# def add_student(student: dict, user=Depends(get_current_user)):
#     student["user_id"] = user["sub"]
#     students_collection.insert_one(student)
#     return {"msg": "Student added"}

# # 🔹 Get My Data
# @router.get("/me")
# def get_my_data(user=Depends(get_current_user)):
#     student = students_collection.find_one({"user_id": user["sub"]})
#     return student

# # 🔹 Get All Students (Admin)
# @router.get("/")
# def get_all_students(user=Depends(get_current_user)):
#     return list(students_collection.find())
from fastapi import APIRouter, Depends
from database import students_collection
from dependencies import get_current_user
from models.student import Student

router = APIRouter(prefix="/students", tags=["Students"])

# 🔹 Add Student
@router.post("/")
def add_student(student: Student, user=Depends(get_current_user)):
    data = student.dict()
    data["user_id"] = user["sub"]

    students_collection.insert_one(data)
    return {"msg": "Student added"}

# 🔹 Get My Profile
@router.get("/me")
def get_my_profile(user=Depends(get_current_user)):
    student = students_collection.find_one({"user_id": user["sub"]})
    
    if not student:
        return {"msg": "No data found"}

    student["_id"] = str(student["_id"])
    return student