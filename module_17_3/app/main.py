# install fastapi, uvicorn, alembic, slugify
#alembic init app/migrations
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
