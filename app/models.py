from sqlalchemy import create_engine, String
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
from contextlib import asynccontextmanager
from fastapi import FastAPI

DATABASE_URL = "sqlite:///production.db"

class Base(DeclarativeBase):
    pass

class DBComic(Base):
    __tablename__ = "comic"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100))
    author: Mapped[int] = mapped_column(String(100))
    description: Mapped[str | None]

class NotFoundError(Exception):
    pass

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield