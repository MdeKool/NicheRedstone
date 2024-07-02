# SQLAlchemy models
from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship, backref

from app.db.config import Base


class Block(Base):
    __tablename__ = "blocks"

    block_id = Column(String, primary_key=True)
    owner = Column(String, ForeignKey("players.username"))
    owner_id = Column(String, ForeignKey("players.uuid"))

    owner = relationship("Player", back_populates="blocks")


class Player(Base):
    __tablename__ = "players"

    uuid = Column(String, primary_key=True)
    username = Column(String)

    blocks = relationship("Block", back_populates="owner")


class Task(Base):
    __tablename__ = "tasks"

    task_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String)
    status = Column(String, default="TO-DO")
    parent_id = Column(Integer, ForeignKey("tasks.task_id"), nullable=True)

    subtasks = relationship("Task", backref=backref("parent", remote_side=[task_id]))

    def __repr__(self):
        return f"<Task {self.task_id}, name: {self.name}, parent: {self.parent_id}, subtasks: {self.subtasks}>"
