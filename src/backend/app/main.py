import logging
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Response, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.session import engine, get_db
from app.repositories.consultas import ItemRepository

logger = logging.getLogger(__name__)


def db_disponible() -> bool:
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except SQLAlchemyError:
        return False


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not db_disponible():
        logger.warning("La app arrancó sin conexión a la base de datos")
    yield
    engine.dispose()


app = FastAPI(lifespan=lifespan)


@app.get("/health")
def health(response: Response):
    if db_disponible():
        return {"status": "ok", "database": "ok"}
    response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return {"status": "degraded", "database": "unavailable"}


@app.get("/api")
def get_mensaje(response: Response, db: Session = Depends(get_db)):
    try:
        repo = ItemRepository(db)
        registro = repo.get_first()
        mensaje = registro.item if registro else "Conexión exitosa a PostgreSQL (tabla vacía)"
        return {"mensaje": mensaje}
    except SQLAlchemyError as e:
        logger.error(f"Error consultando PostgreSQL: {e}")
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"detail": "Base de datos PostgreSQL no disponible o tabla 'item' no creada."}
