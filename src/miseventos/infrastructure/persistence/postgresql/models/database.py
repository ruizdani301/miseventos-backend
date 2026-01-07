from sqlmodel import SQLModel, create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Crear tablas desde todos los modelos SQLModel"""
    # Importa todos tus modelos AQUÍ para que SQLModel los registre
    from .user_model import User
    from .event_model import Event

    from .speaker_model import Speaker
    from .session_model import Session
    from .time_model import TimeSlot
    from .event_registration_model import EventRegistration
    from .session_registration_model import SessionRegistration
    from .session_speaker_model import SessionSpeaker  # Importa todos los modelos
    SQLModel.metadata.create_all(engine)