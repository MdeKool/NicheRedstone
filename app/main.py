from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from sqlalchemy.orm import Session

from app.routers.blocks import blockactions
from app.db.crud import get_blocks
from app.util.db_dependency import get_db
from app.util.secure_url import url_for


app = FastAPI(title="Minecraft WiFi Block", version="0.0.1")

# Add routers
app.include_router(blockactions.router)

# Add mount points for directories outside of app directory
app.mount("/js", StaticFiles(directory="js"), name="scripts")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/styling", StaticFiles(directory="static/styling"), name="styling")
templates = Jinja2Templates(directory="templates")

# templates.env.globals["url_for"] = url_for


@app.get("/")
async def root(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "blocks": get_blocks(db)
        }
    )
