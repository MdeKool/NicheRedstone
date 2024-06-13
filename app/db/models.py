# SQLAlchemy models
from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.config import Base


class Block(Base):
    __tablename__ = "blocks"

    id = Column(Integer, primary_key=True)
    owner = Column(String, ForeignKey("players.username"))
    owner_id = Column(Integer, ForeignKey("players.uuid"))

    owner = relationship("Player", back_populates="blocks")


class Player(Base):
    __tablename__ = "players"

    uuid = Column(Integer, primary_key=True)
    username = Column(String)

    blocks = relationship("Block", back_populates="owner")
