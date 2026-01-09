import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from loguru import logger

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
logger.debug(DATABASE_URL)

engine = create_engine(DATABASE_URL)
Base = declarative_base() # Todos os modelos do ORM herdam do obj Base

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db(): # Cada chamada de get_db criará uma sessão independente
    db = SessionLocal()
    try:
        yield db # Qnd se yield (ao invés de return) a função fica "parada" esperando que o item seja "devolvido"
    finally:
        db.close()

get_db()
