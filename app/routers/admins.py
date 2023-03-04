from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from app.types.models.admins import Admin
from app.utils.database.controllers.admins_controller import admins_controller, GetAdminFilter
from app.security.dependencies import authorize_user, allow_get_requests, allow_create_requests, allow_delete_requests


router = APIRouter(
    prefix='/admins',
    tags=['admins'],
    dependencies=[Depends(authorize_user)],
    responses={status.HTTP_404_NOT_FOUND: {'description': 'Not found'}}
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


@router.get('/')
async def load_base_admins_root():
    """Load base admins root."""

    return "Base admins root processor :)"


@router.get('/get', dependencies=[Depends(allow_get_requests)], response_model=Admin)
async def get_admin(
        admin_id: int | None = Query(
            default=None,
            description='Admin\'s identifier to get his data from database'
        )
):
    """Return admin's data model."""

    if not admin_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Invalid admin id'
        )
    return admins_controller.get_admin(payload=admin_id)


@router.post(
    '/create',
    dependencies=[Depends(allow_create_requests)],
    response_model=Admin,
    response_description='Created admin data model',
    status_code=status.HTTP_201_CREATED
)
async def create_admin(user_form: OAuth2PasswordRequestForm = Depends()):
    """Create admin and return his data model."""

    if admins_controller.is_existing_admin(payload=user_form.username):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Admin already exists'
        )

    created_admin = admins_controller.create_admin(
        username=user_form.username,
        password=user_form.password
    )
    return created_admin


@router.delete('/delete', dependencies=[Depends(allow_delete_requests)])
async def delete_admin(admin_id: int = Query(description='Admin\'s identifier to delete him from database')):
    """Delete provided admin from database."""

    if not admins_controller.is_existing_admin(payload=admin_id, filter_=GetAdminFilter.by_id):
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail='Admin does not exist'
        )
    admins_controller.delete_admin(admin_id=admin_id)
    return {'ok': True}
