from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import ValidationError

from scoorent.data.settings import security_settings
from scoorent.types.models.security import Token, Permissions
from scoorent.utils.security import authenticate_admin, create_access_token


router = APIRouter(
    tags=['jwt token'],
    responses={status.HTTP_401_UNAUTHORIZED: {'description': 'Not authenticated'}}
)


@router.post('/token', response_model=Token)
async def process_generate_token_request(form_data: OAuth2PasswordRequestForm = Depends()):
    """Create access token."""

    try:
        permissions = Permissions.parse_raw(''.join(form_data.scopes))
    except ValidationError:
        permissions = Permissions()

    if not authenticate_admin(username=form_data.username, password=form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'}
        )

    expires = timedelta(minutes=security_settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={'sub': form_data.username},
        permissions=permissions,
        expires_delta=expires
    )
    return {'access_token': access_token, 'token_type': 'bearer'}
