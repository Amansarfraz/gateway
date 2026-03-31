from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

# 🔹 MongoDB ObjectId support
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

# 🔹 Register input
class UserCreate(BaseModel):
    username: str
    password: str
    role: str = "user"  # admin / user / owner

# 🔹 Login input
class UserLogin(BaseModel):
    username: str
    password: str

# 🔹 Response output
class UserResponse(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    username: str
    role: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        # 🔹 Student Model (MongoDB)
class Student(BaseModel):
    name: str
    roll_no: str
    department: str
    semester: int
    user_id: str  # link with login user