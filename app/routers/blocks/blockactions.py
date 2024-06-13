import random

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session as saSession
from app.util.db_dependency import get_db


templates = Jinja2Templates(directory="templates")
router = APIRouter(
    prefix="/blocks"
)

blocks = []


@router.put("/add")
async def add_block(request: Request, db: saSession = Depends(get_db)):
    new_id = random.randint(0, 65535)
    blocks.append(new_id)
    return templates.TemplateResponse(
        "partials/block.html",
        {
            "request": request,
            "id": new_id
        }
    )


@router.put("/remove")
async def remove_block(request: Request, db: saSession = Depends(get_db)):
    data = await request.json()
    block_id = data["blockId"]
    if block_id in blocks:
        print("Removing block with id", block_id)
        blocks.remove(block_id)
        # TODO: REMOVE BLOCK WITH BLOCK_ID FROM DB
        return True
    return False
