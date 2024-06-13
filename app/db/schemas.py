# Pydantic models
from pydantic import BaseModel


class BlockBase(BaseModel):
    pass


class BlockCreate(BlockBase):
    id: int


class Block(BlockBase):
    owner: str
    owner_id: int

    class Config:
        orm_mode = True


class PlayerBase(BaseModel):
    pass


class PlayerCreate(PlayerBase):
    uuid: int
    username: str


class Player(PlayerBase):
    blocks: list[Block] = []

    class Config:
        orm_mode = True
