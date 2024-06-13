import random
import os

from fastapi import APIRouter, Request
from fastapi.responses import FileResponse

router = APIRouter(prefix="/placeholders")

PLACEHOLDER_DIR = "static/placeholders"

placeholders = [file for file in os.listdir(PLACEHOLDER_DIR) if file.endswith(".gif")]


@router.get("/")
async def random_placeholder(request: Request):
    placeholder = random.choice(placeholders)
    path = os.path.join(PLACEHOLDER_DIR, placeholder)
    return FileResponse(path, media_type="image/gif")
