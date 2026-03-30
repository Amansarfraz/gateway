from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

# 🔹 Convert MongoDB ObjectId to string
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

# 🔹 Base User Model
class UserBase(BaseModel):
    username: str
    role: str = "user"  # admin / user / owner

# 🔹 Register Model (input)
class UserCreate(UserBase):
    password: str

# 🔹 Login Model
class UserLogin(BaseModel):
    username: str
    password: str

# 🔹 Response Model (output)
class UserResponse(UserBase):
    id: Optional[PyObjectId] = Field(alias="_id")

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}