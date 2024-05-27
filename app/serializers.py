from sqlalchemy.orm import Session

from app.models import DBComic, NotFoundError
from app.validations import Comic, ComicUpdate, ComicCreate

def db_find_comic(comic_id: int, db: Session) -> DBComic:
    db_comic = db.query(DBComic).filter(DBComic.id == comic_id).first()
    if db_comic is None:
        raise NotFoundError()
    return db_comic

def db_create_comic(comic: ComicCreate, session: Session) -> Comic:
    db_comic = DBComic(**comic.model_dump())
    session.add(db_comic)
    session.commit()
    session.refresh(db_comic)
    return Comic(**db_comic.__dict__)

def db_read_comic(comic_id: int, session: Session) -> Comic:
    db_comic = db_find_comic(comic_id, session)
    return Comic(**db_comic.__dict__)

def db_read_all_comics(session: Session):
    db_comics = session.query(DBComic).all()
    if db_comics is None:
        raise NotFoundError()
    return [Comic(**db_comic.__dict__) for db_comic in db_comics]

def db_update_comic(comic_id: int, comic: ComicUpdate, session: Session) -> Comic:
    db_comic = db_find_comic(comic_id, session)
    for key, value in comic.__dict__.items():
        setattr(db_comic, key, value)
    session.commit()
    session.refresh(db_comic)
    return Comic(**db_comic.__dict__)

def db_delete_comic(comic_id: int, session: Session) -> Comic:
    db_comic = db_find_comic(comic_id, session)
    session.delete(db_comic)
    session.commit()
    return Comic(**db_comic.__dict__)