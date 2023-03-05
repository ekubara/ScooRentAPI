from jose.jwt import decode
from passlib.context import CryptContext

from scoorent.data.settings import security_settings


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_entity(plain_text_entity: str, hashed_entity: str) -> bool:
    return pwd_context.verify(plain_text_entity, hashed_entity)


def hash_entity(entity: str) -> str:
    return pwd_context.hash(entity)


def decode_token(token: str) -> dict:
    return decode(
        token=token,
        key=security_settings.secret_key,
        algorithms=[security_settings.algorithm]
    )
