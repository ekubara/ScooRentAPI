from typing import Union

from fastapi import APIRouter, Body, Depends, Query, status
from fastapi.responses import JSONResponse

from scoorent.exceptions import (
    EmailAlreadyInUse, IncorrectPhoneNumber, ProvideAnyParameter,
    UserAlreadyExists, UserDoesNotExist,
)
from scoorent.types.models.common_models import GoodResponse
from scoorent.types.models.users import InputUser, User
from scoorent.middlewares import prettify_phone_number, is_phone_number
from scoorent.security.dependencies import (
    authorize_user, allow_get_requests, allow_create_requests, allow_delete_requests
)
from scoorent.utils.database.controllers.users_controller import users_controller, GetUserFilter


router = APIRouter(
    tags=['users'],
    dependencies=[Depends(authorize_user)],
    responses={status.HTTP_404_NOT_FOUND: {'description': 'Not found'}}
)


@router.get(
    '/getUser',
    dependencies=[Depends(allow_get_requests)],
    response_description='Selected user data model',
    response_model=Union[User, tuple[User, ...]]
)
async def get_user_data(
        user_id: int | None = Query(
            default=None,
            description='Provide user\'s identifier to get his JSON data model'
        ),
        get_all: bool = Query(
            default=False,
            description='Set `get_all=true` to get all users database has'
        )
):
    """Get user's data model by provided identifier."""

    if not user_id and not get_all:
        raise ProvideAnyParameter

    if user_id:
        if not users_controller.is_user(payload=user_id):
            raise UserDoesNotExist(user_id)
        return users_controller.get_user(payload=user_id)

    if not user_id and get_all:
        return users_controller.get_users()


@router.post(
    '/createUser',
    dependencies=[Depends(allow_create_requests)],
    response_model=User,
    status_code=status.HTTP_201_CREATED
)
async def create_user(
        user_data: InputUser = Body(
            description='User\'s JSON model to create new user',
            example={
                'phoneNumber': '+7 666 555 44 33',
                'firstName': 'Роман',
                'lastName': 'Першиков',
                'email': 'romkathebestdev@gmail.com'
            }
        )
):
    """Create a user."""

    if not is_phone_number(user_data.phone_number):
        raise IncorrectPhoneNumber(user_data.phone_number)

    user_data.phone_number = prettify_phone_number(user_data.phone_number)

    if users_controller.is_user(payload=user_data.phone_number, filter_=GetUserFilter.by_phone_number):
        raise UserAlreadyExists(
            user_id=users_controller.get_user(
                payload=user_data.phone_number,
                filter_=GetUserFilter.by_phone_number
            ).id
        )

    if users_controller.is_user(payload=user_data.email, filter_=GetUserFilter.by_email):
        raise EmailAlreadyInUse(user_data.email)

    created_user = users_controller.create_user(user=user_data)
    return created_user


@router.delete('/deleteUser', response_model=GoodResponse, dependencies=[Depends(allow_delete_requests)])
async def delete_user(user_id: int = Query(description='User\'s identifier to delete him from database')):
    """Delete user from service's database."""

    if not users_controller.is_user(payload=user_id):
        raise UserDoesNotExist(user_id)
    users_controller.delete_user(user_id)
    return GoodResponse()
