from . import database


def get_db():
    db: database.Session = database.SessionLocal()
    yield db
    db.close()