from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Linux DB url
SQLALCHEMY_DATABASE_URL = "sqlite:////var/opt/db/ServerBlock.db"

# Windows DB url
# SQLALCHEMY_DATABASE_URL = "sqlite:///.database/ServerBlock.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
