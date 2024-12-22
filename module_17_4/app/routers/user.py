from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated

from app.models.user import User
from app.models.task import Task
from app.schemas import CreateUser, UpdateUser
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/")
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User)).all()
    if users == []:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Table is empty'
        )
    return users

@router.get("/{user_id}")
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User id({user_id}) not found'
        )
    return user

@router.post("/create")
async def create_user(db: Annotated[Session, Depends(get_db)], create_user: CreateUser):
    db.execute(insert(User).values(username=create_user.username,
                                   firstname=create_user.firstname,
                                   lastname=create_user.lastname,
                                   age=create_user.age,
                                   slug=slugify(create_user.username)))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }

@router.put("/update/{user_id}")
async def update_user(db: Annotated[Session, Depends(get_db)], user_id, update_user: UpdateUser):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User id({user_id}) not found'
        )
    db.execute(update(User).where(User.id == user_id).values(
                                   firstname=update_user.firstname,
                                   lastname=update_user.lastname,
                                   age=update_user.age))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User update is successful!'
    }

@router.delete("/delete/{user_id}")
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User id({user_id}) not found'
        )
    db.execute(delete(Task).where(Task.user_id == user_id))
    db.execute(delete(User).where(User.id == user_id))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User deleted is successful!'
    }

@router.get("/{user_id}/tasks")
async def all_users(db: Annotated[Session, Depends(get_db)], user_id):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User id({user_id}) not found'
        )

    tasks = db.scalars(select(Task).where(Task.user_id == user_id)).all()
    if tasks == []:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Tasks not found'
        )
    return tasks
