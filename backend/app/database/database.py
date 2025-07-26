from typing import Any
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm.session import Session
import os


engine: Engine = create_engine(url=f"postgresql://{os.environ.get("POSTGRES_USER", default="")}:{os.environ.get("POSTGRES_PASSWORD", default="")}@localhost:5432/taskprojectmanager")
SessionLocal: sessionmaker[Session] = sessionmaker(bind=engine, autoflush=True)
Base: Any = declarative_base()