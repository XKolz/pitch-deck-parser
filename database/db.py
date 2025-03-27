import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base

def get_engine():
    db_url = os.getenv('DB_URL', 'postgresql://user:password@db:5432/pitchdeck')
    return create_engine(db_url)

engine = get_engine()
# SessionLocal = sessionmaker(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(engine)
