from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from todo_app import crud
from todo_app.database import Base, engine, get_db
from todo_app.schemas import TodoCreate, TodoOut, TodoUpdate


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/todos", response_model=TodoOut)
async def create_todo(data: TodoCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_todo(db, data)


@app.get("/todos", response_model=list[TodoOut])
async def list_todos(db: AsyncSession = Depends(get_db)):
    return await crud.list_todos(db)


@app.get("/todos/{todo_id}", response_model=TodoOut)
async def get_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    todo = await crud.get_todo(db, todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.put("/todos/{todo_id}", response_model=TodoOut)
async def update_todo(todo_id: int, data: TodoUpdate, db: AsyncSession = Depends(get_db)):
    todo = await crud.get_todo(db, todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return await crud.update_todo(db, todo, data)


@app.delete("/todos/{todo_id}", status_code=204)
async def delete_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    todo = await crud.get_todo(db, todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    await crud.delete_todo(db, todo)
