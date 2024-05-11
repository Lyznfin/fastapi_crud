from pydantic import BaseModel

class Comic(BaseModel):
    id: int
    title: str
    author: str
    description: str | None

class ComicCreate(BaseModel):
    title: str
    author: str
    description: str | None

class ComicUpdate(BaseModel):
    title: str | None
    author: str | None
    description: str | None