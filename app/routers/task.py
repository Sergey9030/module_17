from fastapi import APIRouter

router = APIRouter(prefix="/task", tags=["task"])

@router.get("/")
async def all_tasks():
    pass

@router.get("/{task_id}")
async def task_by_id():
    pass

@router.post("/create")
async def create_tack():
    pass

@router.put("/update/{task_id}")
async def update_task():
    pass

@router.delete("/delete/{task_id}")
async def delete_task():
    pass

