from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from todo_app.models import Todo
from todo_app.schemas import TodoCreate, TodoUpdate


async def create_todo(db: AsyncSession, data: TodoCreate) -> Todo:
    todo = Todo(title=data.title)
    db.add(todo)
    await db.commit()
    await db.refresh(todo)
    return todo


async def get_todo(db: AsyncSession, todo_id: int) -> Todo | None:
    result = await db.execute(select(Todo).where(Todo.id == todo_id))
    return result.scalar_one_or_none()


async def list_todos(db: AsyncSession) -> list[Todo]:
    result = await db.execute(select(Todo))
    return list(result.scalars().all())


async def update_todo(db: AsyncSession, todo: Todo, data: TodoUpdate) -> Todo:
    if data.title is not None:
        todo.title = data.title
    if data.done is not None:
        todo.done = data.done
    await db.commit()
    await db.refresh(todo)
    return todo


async def delete_todo(db: AsyncSession, todo: Todo) -> None:
    await db.delete(todo)
    await db.commit()
