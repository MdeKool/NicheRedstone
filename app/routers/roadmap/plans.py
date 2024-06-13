from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.util.db_dependency import get_db

router = APIRouter(prefix="/plans")
templates = Jinja2Templates(directory="templates")


@router.get("/")
def root(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse(
        "partials/404.html",  # TODO: Create plans page
        {
            "request": request,
        }
    )
