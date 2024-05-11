from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker, Session

from app.routers import app
from app.models import get_db, Base, DBComic

# pytest app/tests.py

DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    database = TestingSessionLocal()
    yield database
    database.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def session():
    Base.metadata.create_all(bind=engine)
    db_session = TestingSessionLocal()

    db_comic = DBComic(id=1, title="Test title", author="Test author", description="This is a test comic")
    db_session.add(db_comic)

    db_comic2 = DBComic(id=2, title="Test title", author="Test author", description="This is a test comic")
    db_session.add(db_comic2)

    db_session.commit()

    yield db_session

    db_session.close()
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)

def test_create_comic(session: Session):
    response = client.post("/comic/", json={"title": "Test title", "author": "Test author", "description": "This is a test comic"})
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["title"] == "Test title"
    assert data["author"] == "Test author"
    assert data["description"] == "This is a test comic"
    assert "id" in data

def test_read_all_comic(session: Session):
    response = client.get(f"/comic/all")
    datas = response.json()
    for data in datas:
        assert data["title"] == "Test title"
        assert data["author"] == "Test author"
        assert data["description"] == "This is a test comic"

def test_read_comic(session: Session):
    comic_id = 1
    response = client.get(f"/comic/{comic_id}")
    data = response.json()
    assert data["title"] == "Test title"
    assert data["author"] == "Test author"
    assert data["description"] == "This is a test comic"

def test_update_comic(session: Session):
    comic_id = 1
    response = client.put(
        f"/comic/{comic_id}",
        json={"title": "Updated test title", "author": "Updated test author", "description": "This is an updated test comic"},
    )
    assert response.status_code == 200, response.text
    
    data = response.json()
    assert data["title"] == "Updated test title"
    assert data["author"] == "Updated test author"
    assert data["description"] == "This is an updated test comic"
    assert data["id"] == comic_id

def test_delete_comic(session: Session):
    comic_id = 1
    response = client.delete(f"/comic/{comic_id}")
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["id"] == comic_id

    response = client.get(f"/comic/{comic_id}")
    assert response.status_code == 404, response.text