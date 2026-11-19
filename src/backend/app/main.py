import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Response, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.db.session import engine

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
def get_mensaje(response: Response):
    try:
        with engine.connect() as conn:
            # Consulta el mensaje persistido en PostgreSQL
            result = conn.execute(text("SELECT contenido FROM mensajes LIMIT 1")).fetchone()
            mensaje = result[0] if result else "Conexión exitosa a PostgreSQL (tabla vacía)"
            return {"mensaje": mensaje}
    except SQLAlchemyError as e:
        logger.error(f"Error consultando PostgreSQL: {e}")
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"detail": "Base de datos PostgreSQL no disponible o tabla 'mensajes' no creada."}