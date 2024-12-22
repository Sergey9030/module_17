# install: fastapi, uvicorn, alembic, python-slugify
#alembic init app/migrations

#alembic.ini 64:sqlalchemy.url = sqlite:///taskmanager.db

#env.py:
#22:from app.backend.db import Base
#23:from app.models.user import User
#24:from app.models.task import Task
#25:target_metadata = Base.metadata

#alembic revision --autogenerate -m "Initial migration"
#alembic upgrade head

# python -m uvicorn app.main:app

from fastapi import FastAPI
from app.routers import task, user


app = FastAPI()

@app.get("/")
async def welcome():
    return {"message": "Welcome to Taskmanager"}

app.include_router(task.router)
app.include_router(user.router)
