from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from miseventos.infrastructure.persistence.postgresql.models.event_model import Event
from miseventos.infrastructure.persistence.postgresql.models.session_model import (
    Session,
)
from miseventos.infrastructure.persistence.postgresql.models.speaker_model import (
    Speaker,
)
from miseventos.infrastructure.persistence.postgresql.models.session_speaker_model import (
    SessionSpeaker,
)
from miseventos.infrastructure.persistence.postgresql.models.session_registration_model import (
    SessionRegistration,
)
from miseventos.infrastructure.persistence.postgresql.models.event_registration_model import (
    EventRegistration,
)
from miseventos.infrastructure.persistence.postgresql.models.time_model import TimeSlot
from miseventos.infrastructure.persistence.postgresql.models.user_model import User

# ---- CONFIGURAR RUTAS ----
# Ruta al directorio que contiene alembic.ini (la raíz del proyecto)
project_root = Path(__file__).parent.parent  # misEventos/

# Cargar .env desde la raíz
env_path = project_root / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
    print(f"✅ .env cargado desde: {env_path}")
else:
    print(f"⚠️  .env no encontrado en: {env_path}")
    load_dotenv()

# Agregar ruta a src/miseventos para importar tu código
app_path = project_root / "src" / "miseventos"
sys.path.insert(0, str(app_path))

# ---- IMPORTAR BASE DE DATOS ----
try:
    # Importa Base desde tu database.py
    from miseventos.infrastructure.persistence.postgresql.models.database import Base

    print("✅ Base importada correctamente")
except ImportError as e:
    print(f"❌ Error importando Base: {e}")
    print(f"   Ruta intentada: {app_path}")
    raise

# ---- CONFIGURACIÓN ALEMBIC ----
config = context.config

# Usar DATABASE_URL del .env si existe
database_url = os.getenv("DATABASE_URL")
if database_url:
    config.set_main_option("sqlalchemy.url", database_url)
    print(f"✅ Usando DATABASE_URL del .env")
else:
    print("ℹ️  Usando sqlalchemy.url de alembic.ini")

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ---- CONFIGURAR METADATAS ----
target_metadata = Base  # ← ¡ESTO ES CLAVE!


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
