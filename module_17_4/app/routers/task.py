from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated

from app.models.task import Task
from app.models.user import User
from app.schemas import CreateTask, UpdateTask
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(prefix="/task", tags=["task"])

@router.get("/")
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task)).all()
    if tasks == []:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Table is empty'
        )
    return tasks

@router.get("/{task_id}")
async def task_by_id(db: Annotated[Session, Depends(get_db)], task_id):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Task id({task_id}) not found'
        )
    return task

@router.post("/create")
async def create_tack(db: Annotated[Session, Depends(get_db)], user_id, create_task: CreateTask):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User id({user_id}) not found'
        )
    db.execute(insert(Task).values(title=create_task.title,
                                   content=create_task.content,
                                   user_id=user_id,
                                   priority=create_task.priority,
                                   slug=slugify(create_task.title)))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }

@router.put("/update/{task_id}")
async def update_task(db: Annotated[Session, Depends(get_db)], task_id, update_task: UpdateTask):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Task id({task_id}) not found'
        )
    db.execute(update(Task).where(Task.id == task_id).values(
                                   title=update_task.title,
                                   content=update_task.content,
                                   priority=update_task.priority,
                                   slug=slugify(update_task.title)))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User update is successful!'
    }

@router.delete("/delete/{task_id}")
async def delete_task(db: Annotated[Session, Depends(get_db)], task_id):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Task id({task_id}) not found'
        )
    db.execute(delete(Task).where(Task.id == task_id))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Task deleted is successful!'
    }

