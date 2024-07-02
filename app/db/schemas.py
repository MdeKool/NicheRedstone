# Pydantic models
from pydantic import BaseModel, Field
from typing import List, Optional, ClassVar


class BlockBase(BaseModel):
    pass


class BlockCreate(BlockBase):
    block_id: str


class Block(BlockBase):
    owner: str
    owner_id: str

    class Config:
        from_attributes = True


class PlayerBase(BaseModel):
    pass


class PlayerCreate(PlayerBase):
    uuid: str
    username: str


class Player(PlayerBase):
    blocks: list[Block] = []

    class Config:
        from_attributes = True


class TaskBase(BaseModel):
    pass


class TaskCreate(TaskBase):
    name: str
    description: Optional[str]


class Task(TaskBase):
    task_id: int
    status: str
    subtasks: List["Task"] = Field(default_factory=list)

    class Config:
        from_attributes = True


class TaskUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    status: Optional[str]

    class Config:
        from_attributes = True


Task.model_rebuild()
