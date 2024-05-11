from fastapi import FastAPI, HTTPException
from fastapi.params import Depends

from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.models import NotFoundError, get_db, lifespan
from app.authentications import ComicCreate, ComicUpdate, Comic
from app.serializers import db_create_comic, db_read_all_comics, db_read_comic, db_update_comic, db_delete_comic

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def redirect():
    response = RedirectResponse(url="/comic/all")
    return response

@app.post("/comic/")
def create_comic(comic: ComicCreate, db: Session = Depends(get_db)) -> Comic:
    return db_create_comic(comic, db)

@app.get("/comic/all")
def read_all_comics(db: Session = Depends(get_db)) -> list[Comic]:
    try:
        return db_read_all_comics(db)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Comic not found")

@app.get("/comic/{comic_id}")
def read_comic(comic_id: int, db: Session = Depends(get_db)) -> Comic:
    try:
        return db_read_comic(comic_id, db)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Comic not found")

@app.put("/comic/{comic_id}")
def update_comic(comic_id: int, comic: ComicUpdate, db: Session = Depends(get_db)) -> Comic:
    try:
        return db_update_comic(comic_id, comic, db)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Comic not found")

@app.delete("/comic/{comic_id}")
def delete_comic(comic_id: int, db: Session = Depends(get_db)) -> Comic:
    try:
        return db_delete_comic(comic_id, db)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Comic not found")