from collections.abc import Generator

from app.database.database import SessionLocal


def get_db() -> Generator:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()