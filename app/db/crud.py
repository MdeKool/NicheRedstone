from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db import models, schemas


def get_player(db: Session, uuid: str):
    return db.query(models.Player).filter(models.Player.uuid == uuid).first()


def get_player_by_username(db: Session, username: str):
    return db.query(models.Player).filter(models.Player.username == username).first()


def get_players(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Player).offset(skip).limit(limit).all()


def create_player(db: Session, player: schemas.PlayerCreate):
    db_player = models.Player(uuid=player.uuid, username=player.username)
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player


def get_blocks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Block).offset(skip).limit(limit).all()


def get_block_by_id(db: Session, block_id: str):
    return db.query(models.Block).filter(models.Block.id == block_id).first()


def create_block(db: Session, block: schemas.BlockCreate, owner_id: str):
    db_block = models.Block(**block.dict(), owner_id=owner_id)
    db.add(db_block)
    db.commit()
    db.refresh(db_block)
    return db_block


def create_task(db: Session, task: schemas.TaskCreate, parent_id: int = None):
    db_task = models.Task(**task.dict(), parent_id=parent_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Task).offset(skip).limit(limit).all()


def update_task_status(db: Session, task_id: int, update: schemas.TaskUpdate):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(404, "Task not found")

    for key, value in update.dict(exclude_unset=True).items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return task
