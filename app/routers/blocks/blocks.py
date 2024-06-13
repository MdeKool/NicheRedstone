import random

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session as saSession

from app.util.db_dependency import get_db
from app.db.schemas import BlockCreate
from app.db.crud import create_block, get_blocks, get_block_by_id


templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/blocks")


@router.get("/")
async def root(request: Request, db: saSession = Depends(get_db)):
    return templates.TemplateResponse(
        "blocks.html", {"request": request, "blocks": get_blocks(db)}
    )


@router.put("/add")
async def add_block(request: Request, db: saSession = Depends(get_db)):
    block = create_block(
        db,
        block=BlockCreate(id=random.randint(1, 65535)),
        owner_id=random.choice([_ for _ in range(4)]),
    )
    return templates.TemplateResponse(
        "partials/block.html",
        {"request": request, "id": block.id, "owner_id": block.owner_id},
    )


@router.put("/remove")
async def remove_block(request: Request, db: saSession = Depends(get_db)):
    data = await request.json()
    block_id = data["blockId"]

    block = get_block_by_id(db, block_id)

    if block:
        db.delete(block)
        db.commit()
        return True
    return False
