import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./netragati_local.db")
USE_SQLITE = os.getenv("USE_SQLITE_FALLBACK", "True").lower() == "true"

if USE_SQLITE and not DATABASE_URL.startswith("postgresql"):
    DATABASE_URL = f"sqlite:///{os.getenv('SQLITE_DB_PATH', './netragati_local.db')}"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    try:
        engine = create_engine(DATABASE_URL, pool_size=20, max_overflow=10, pool_pre_ping=True)
    except Exception:
        DATABASE_URL = "sqlite:///./netragati_local.db"
        engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
