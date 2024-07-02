import random

import httpx
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session as saSession

import hashlib

from app.util.db_dependency import get_db
from app.db.schemas import BlockCreate
from app.db.crud import create_block, get_blocks, get_block_by_id


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
    m = hashlib.sha3_384()
    m.update(bytes(data["block_id"].encode()))
    hash_id = m.hexdigest()
    if get_block_by_id(db, hash_id):
        raise HTTPException(400, "Block already registered")
    create_block(
        db,
        block=BlockCreate(block_id=hash_id),
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
    async with httpx.AsyncClient() as client:
        if await client.post("http://192.168.0.107:8080/callback", json=data) == 200:
            return {"success": True}
        return {"success": False}


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
