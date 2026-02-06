from sqlalchemy import orm
from miseventos.repositories.session_register_repository import (
    SessionRegisterRepository,
)
from miseventos.infrastructure.persistence.postgresql.models.session_model import (
    Session as SessionModel,
)
from miseventos.infrastructure.persistence.postgresql.models.user_model import User
from miseventos.infrastructure.persistence.postgresql.models.event_model import Event
from miseventos.infrastructure.persistence.postgresql.models.event_registration_model import (
    EventRegistration,
)
from miseventos.infrastructure.persistence.postgresql.models.session_registration_model import (
    SessionRegistration,
)
from miseventos.infrastructure.persistence.postgresql.models.session_model import (
    Session,
)
from miseventos.infrastructure.persistence.postgresql.schemas.session_register_schema import (
    SessionRegisterRequest,
    registerResponse,
    SessionDeleteResponse,
    SessionRegisterDeleteRequest,
)
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError


class SessionRegisterImplement(SessionRegisterRepository):
    def __init__(self, session: orm.Session):
        self.session: orm.Session = session

    def add_session_register(self, body: SessionRegisterRequest) -> registerResponse:
        try:
            user = self.session.get(User, body.user_id)
            if not user:
                return registerResponse(success=False, message="Usuario no encontrado")

            event = self.session.get(Event, body.event_id)
            if not event:
                return registerResponse(success=False, message="Evento no encontrado")

            session = self.session.get(Session, body.session_id)
            if not session:
                return registerResponse(success=False, message="Sesión no encontrada")

            if session.event_id != body.event_id:
                return registerResponse(
                    success=False,
                    message="La sesión no pertenece al evento especificado",
                )
            event_registration = (
                self.session.query(EventRegistration)
                .filter(
                    and_(
                        EventRegistration.user_id == body.user_id,
                        EventRegistration.event_id == body.event_id,
                    )
                )
                .first()
            )

            if not event_registration:
                # Crear registro en el evento
                event_registration = EventRegistration(
                    user_id=body.user_id, event_id=body.event_id
                )
                self.session.add(event_registration)
                self.session.flush()
            event_registration_id = event_registration.id

            existing_session_reg = (
                self.session.query(SessionRegistration)
                .filter(
                    and_(
                        SessionRegistration.user_id == body.user_id,
                        SessionRegistration.session_id == body.session_id,
                    )
                )
                .first()
            )

            if existing_session_reg:
                return registerResponse(
                    success=False, message="Ya estás registrado en esta sesión"
                )

            session_registration = SessionRegistration(
                user_id=body.user_id, session_id=body.session_id
            )
            self.session.add(session_registration)

            self.session.flush()

            session_registration_id = session_registration.id

            session_reg_count = (
                self.session.query(SessionRegistration)
                .filter(SessionRegistration.session_id == body.session_id)
                .count()
            )

            event_reg_count = (
                self.session.query(EventRegistration)
                .filter(EventRegistration.event_id == body.event_id)
                .count()
            )

            self.session.commit()

            return registerResponse(
                id=str(session_registration_id),
                event_registration_id=str(event_registration_id),
                session_id=str(body.session_id),
                event_id=str(body.event_id),
                number_registered=session_reg_count,
                success=True,
                message="Registro exitoso",
            )

        except IntegrityError as e:
            self.session.rollback()
            # Verificar si es por duplicado en sesión o evento
            if "uq_user_session" in str(e).lower():
                return registerResponse(
                    success=False, message="Ya estás registrado en esta sesión"
                )
            elif "uq_user_event" in str(e).lower():
                return registerResponse(
                    success=False, message="Ya estás registrado en este evento"
                )
            return registerResponse(
                success=False,
                message="Violación de restricción única en la base de datos",
            )

        except Exception as e:
            self.session.rollback()
            return registerResponse(
                success=False, message=f"Error interno del servidor: {str(e)}"
            )

    def delete_session_register(
        self, body: SessionRegisterDeleteRequest
    ) -> SessionDeleteResponse:
        try:
            session_registration = (
                self.session.query(SessionRegistration)
                .filter(
                    and_(
                        SessionRegistration.user_id == body.user_id,
                        SessionRegistration.id == body.register_id,
                    )
                )
                .first()
            )

            if not session_registration:
                return SessionDeleteResponse(
                    success=False, message="No estás registrado en esta sesión"
                )
            registration_id = str(session_registration.id)

            self.session.delete(session_registration)
            self.session.commit()

            return SessionDeleteResponse(
                success=True,
                message="Registro eliminado exitosamente",
                id=registration_id,
            )
        except Exception as e:
            self.session.rollback()
            return SessionDeleteResponse(
                success=False, message=f"Error interno al eliminar el registro"
            )
