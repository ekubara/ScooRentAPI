from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from scoorent.types.models.admins import Admin
from scoorent.types.models.common_models import GoodResponse
from scoorent.utils.database.controllers.admins_controller import admins_controller, GetAdminFilter
from scoorent.security.dependencies import (
    authorize_user, allow_get_requests, allow_create_requests, allow_delete_requests
)


router = APIRouter(
    tags=['Admins'],
    dependencies=[Depends(authorize_user)]
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


@router.get(
    '/getAdmin',
    dependencies=[Depends(allow_get_requests)],
    response_model=Admin
)
async def get_admin(
        admin_id: int | None = Query(
            default=None,
            description='ID of an admin to get his data.'
        )
):
    """Return data of a provided admin."""

    if not admin_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Admin does not exist.'
        )
    return admins_controller.get_admin(payload=admin_id)


@router.post(
    '/createAdmin',
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(allow_create_requests)],
)
async def create_admin(user_form: OAuth2PasswordRequestForm = Depends()):
    """Create admin."""

    if admins_controller.is_existing_admin(payload=user_form.username):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Admin already exists.'
        )
    return GoodResponse()


@router.delete(
    '/deleteAdmin',
    response_model=GoodResponse,
    dependencies=[Depends(allow_delete_requests)]
)
async def delete_admin(admin_id: int = Query(description='ID of an admin to delete.')):
    """Delete admin."""

    if not admins_controller.is_existing_admin(payload=admin_id, filter_=GetAdminFilter.by_id):
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail='Admin does not exist'
        )
    admins_controller.delete_admin(admin_id=admin_id)
    return GoodResponse()
