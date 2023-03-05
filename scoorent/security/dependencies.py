from fastapi import Depends, HTTPException, status
from jose.jwt import JWTError

from . import oauth2_scheme
from scoorent.types.models.security import TokenData
from scoorent.middlewares.security import decode_token
from scoorent.utils.database.controllers.admins_controller import admins_controller


def authorize_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not resolve credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    try:
        payload = decode_token(token=token)
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = TokenData(**payload)
    except JWTError:
        raise credentials_exception
    if not admins_controller.is_existing_admin(payload=token_data.sub):
        raise credentials_exception


class RightsChecker:
    """Dependency to check client's rights."""

    def __init__(self, token: str = Depends(oauth2_scheme)):
        self.token = token
        self.token_data: TokenData | None = None
        self.not_allowed_exception = HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail='You are not allowed to use this method',
            headers={'WWW-Authenticate': 'Bearer'}
        )
        try:
            self.token_payload = decode_token(self.token)
            username: str = self.token_payload.get('sub')
            if username is None:
                raise self.not_allowed_exception
            self.token_data = TokenData(**self.token_payload)
        except JWTError:
            raise self.not_allowed_exception
        if not admins_controller.is_existing_admin(payload=self.token_data.sub):
            raise self.not_allowed_exception


async def allow_get_requests(commons: RightsChecker = Depends()):
    if not commons.token_data.can_get:
        raise commons.not_allowed_exception


async def allow_create_requests(commons: RightsChecker = Depends()):
    if not commons.token_data.can_create:
        raise commons.not_allowed_exception


async def allow_delete_requests(commons: RightsChecker = Depends()):
    if not commons.token_data.can_delete:
        raise commons.not_allowed_exception
