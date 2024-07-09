import random

import httpx
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session as saSession

from app.util.db_dependency import get_db
from app.db.schemas import BlockCreate
from app.db.crud import create_block, get_blocks, get_block_by_id
from app.util.serializer import serialize, deserialize

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/blocks")


@router.get("/")
async def root(request: Request, db: saSession = Depends(get_db)):
    return templates.TemplateResponse(
        "partials/blocks.html", {"request": request, "blocks": get_blocks(db)}
    )


@router.post("/register")
async def register_block(request: Request, db: saSession = Depends(get_db)):
    data = await request.json()
    coordinates = list(map(int, data["block_id"].split(", ")))
    serialized_id = serialize(*coordinates)
    if get_block_by_id(db, serialized_id):
        raise HTTPException(400, "Block already registered")
    create_block(
        db,
        block=BlockCreate(block_id=serialized_id),
        owner_id=data["player_uuid"],
    )
    return True


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


@router.post("/signal")
async def send_pulse(request: Request, db: saSession = Depends(get_db)):
    data = await request.json()
    data["block_id"] = deserialize(data["block_id"])
    async with httpx.AsyncClient() as client:
        return (await client.post("http://172.18.0.2:25567/signal", json=data)).is_success


@router.put("/remove")
async def remove_block(request: Request, db: saSession = Depends(get_db)):
    data = await request.json()
    block_id = data["block_id"]

    block = get_block_by_id(db, block_id)

    if block:
        db.delete(block)
        db.commit()
        return True
    return False
