from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db.crud import create_task as db_create_task, get_root_tasks
from app.db.schemas import TaskCreate
from app.util.db_dependency import get_db

router = APIRouter(prefix="/plans")
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def root(request: Request, db: Session = Depends(get_db)):
    tasks = get_root_tasks(db)
    return templates.TemplateResponse(
        "partials/roadmap.html",
        {"request": request, "tasks": tasks},
    )


@router.put("/new")
async def create_task(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    task_name = data["task_name"]
    task_desc = data["task_description"] if data["task_description"] else None
    try:
        task_parent = data["task_parent"]
    except KeyError:
        task_parent = None
    if db_create_task(
        db,
        task=TaskCreate(name=task_name, description=task_desc),
        parent_id=task_parent,
    ):
        return {"success": True}
    return {"success": False}


@router.post("/new")
async def add_task(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse(
        "partials/tasks/new_task.html",
        {
            "request": request,
        },
    )
