from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix='/tasks',tags=['Tasks'])

class Task(BaseModel):
    title: str
    desc: str

@router.get('/')
async def get_tasks():
    return {"message":"Barcha tasklar","tasks":["Task 1","Task 2","Task 3"]}

@router.post("/")
async def add_task(task: Task):
    return {"message":"Task qo'shildi"}
