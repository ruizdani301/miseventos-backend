from fastapi import FastAPI
from miseventos.infrastructure.persistence.postgresql.models import *
from miseventos.infrastructure.persistence.postgresql.models.database import (
    create_tables,
)

# from .infrastructure.api.routes import user_router
from miseventos.infrastructure.api.routes.user_routes import user_router
from miseventos.infrastructure.api.routes.event_routes import event_router
from miseventos.infrastructure.api.routes.slot_routes import slot_router
from miseventos.infrastructure.api.routes.session_routes import session_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from miseventos.infrastructure.api.routes.speaker_routes import speaker_router

create_tables()


app = FastAPI(title="Mis Eventos")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # En desarrollo permite todos, en producción especifica dominios
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los headers
)
app.include_router(router=user_router, prefix="/api/v1")
app.include_router(router=event_router, prefix="/api/v1")
app.include_router(router=slot_router, prefix="/api/v1")
app.include_router(router=session_router, prefix="/api/v1")
app.include_router(router=speaker_router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {"message": "Welcome to misEventos API"}
