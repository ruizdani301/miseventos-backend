import bcrypt


def encrypt_password(password: str) -> str:
    """
    Encripta una contraseña usando bcrypt.

    Args:
        password: Contraseña en texto plano

    Returns:
        str: Hash de la contraseña en formato string
    """
    password_bytes = password.encode("utf-8")

    salt = bcrypt.gensalt()

    hashed = bcrypt.hashpw(password_bytes, salt)

    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si una contraseña coincide con el hash almacenado.

    Args:
        plain_password: Contraseña en texto plano a verificar
        hashed_password: Hash almacenado en la base de datos

    Returns:
        bool: True si la contraseña es correcta
    """
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )
    except Exception:
        return False
