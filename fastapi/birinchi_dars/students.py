from fastapi import APIRouter
from pydantic import BaseModel


router =  APIRouter(prefix="/students",tags=["Students"])

class Student(BaseModel):
    first_name: str
    last_name: str

@router.get("/")
async def get_students():
    return {"message":"Barcha talabalar ro'yxati","students":['Student 1','Student 2']}

@router.post("/")
async def add_student(student: Student):
    return {"message":"Student qo'shildi","student":student}