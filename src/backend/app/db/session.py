from collections.abc import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from app.core.config import settings

engine = create_engine(
    settings.database_url,
    pool_size=5,        # Permanently opened connections
    max_overflow=10,    # Extra connections when load peaks
    pool_pre_ping=True, # Checks if the connection is still alive before using it again
    pool_recycle=1800,  # Renew connections every 30 minutes.
    connect_args={"connect_timeout": 10}
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        