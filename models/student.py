from pydantic import BaseModel

class Student(BaseModel):
    name: str
    roll_no: str
    department: str
    semester: int