from dataclasses import dataclass
from miseventos.infrastructure.persistence.postgresql.models.enum import RoleName


@dataclass
class UserEntity:
    id: int | None = None
    email: str = ""
    password: str = ""
    role: str = RoleName.ASSISTANT.value

    def valid_password(self):
        if not self.password:
            return False, "La contraseña no puede estar vacía"

        if len(self.password) < 5:
            return False, "La contraseña debe tener al menos 5 caracteres"
        if len(self.password) > 8:
            return False, "La contraseña no puede tener más de 8 caracteres"

        if not self.password.isalnum():
            return False, "La contraseña solo puede contener letras y números"
        return True, "Contraseña válida"
