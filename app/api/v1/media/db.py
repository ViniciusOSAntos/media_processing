import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase
from loguru import logger
from typing import Generator

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
logger.debug(DATABASE_URL)

if DATABASE_URL is None:
    raise ValueError("Database URL Required")
engine = create_engine(DATABASE_URL)

# Base = declarative_base() # Todos os modelos do ORM herdam do obj Base
class Base(DeclarativeBase):
    pass

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]: # Cada chamada de get_db criará uma sessão independente
    db = SessionLocal()
    try:
        yield db # Qnd se yield (ao invés de return) a função fica "parada" esperando que o item seja "devolvido"
    finally:
        db.close()
