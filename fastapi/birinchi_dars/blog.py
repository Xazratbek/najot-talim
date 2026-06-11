from fastapi import APIRouter
from pydantic import BaseModel

class Blog(BaseModel):
    title: str
    desc: str
    author: str

router = APIRouter(prefix="/blog",tags=["Blog"])

@router.get("/")
async def get_posts():
    return {"message":"Barcha postlar","posts":['Post 1','Post 2','Post 3']}

@router.post("/")
async def add_posts(post: Blog):
    return {"message":"Post qo'shildi","post" : post}