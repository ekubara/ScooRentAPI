from datetime import datetime, timedelta

from jose import jwt

from scoorent.data.settings import security_settings
from scoorent.types.models.security import Permissions
from scoorent.middlewares.security import verify_entity
from scoorent.utils.database.controllers.admins_controller import admins_controller


def create_access_token(
        data: dict,
        permissions: Permissions = Permissions(),
        expires_delta: timedelta | None = None
) -> str:
    """Create and return JWT access token."""

    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta if expires_delta else datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({'exp': expire})
    to_encode.update(**permissions.dict())
    encoded_jwt = jwt.encode(to_encode, security_settings.secret_key, algorithm=security_settings.algorithm)
    return encoded_jwt


def authenticate_admin(username: str, password: str) -> bool:
    internal_admin_model = admins_controller.collect_internal_admin_model(username=username)
    if verify_entity(plain_text_entity=password, hashed_entity=internal_admin_model.password):
        return True
    return False
