from typing import Union

from fastapi import APIRouter, Body, Depends, HTTPException, Query, status

from scoorent.exceptions.globals import ProvideAnyParameter
from scoorent.exceptions.users import UserDoesNotExist
from scoorent.security.dependencies import (
    authorize_user, allow_get_requests, allow_create_requests, allow_delete_requests
)
from scoorent.types.models.common_models import GoodResponse
from scoorent.types.models.scooters import Scooter, InputScooterName
from scoorent.utils.database.controllers.scooters import scooters_controller
from scoorent.utils.database.controllers.users import users_controller


router = APIRouter(
    tags=['Scooters'],
    dependencies=[Depends(authorize_user)]
)


@router.get(
    '/getScooter',
    dependencies=[Depends(allow_get_requests)],
    response_model=Union[Scooter, tuple[Scooter, ...]]
)
async def get_scooter(
        scooter_id: int = Query(
            default=None,
            description='ID of a scooter to get its data.'
        ),
        get_all: bool = Query(
            default=False,
            description='Set `get_all=True` to get all scooters data database has.'
        )
):
    """Return scooter's data."""

    if (scooter_id is None) and (get_all is None):
        raise ProvideAnyParameter

    if scooter_id is not None:
        if not scooters_controller.is_scooter(scooter_id=scooter_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Scooter does not exist'
            )
        return scooters_controller.get_scooter(scooter_id=scooter_id)

    if (scooter_id is None) and (get_all is not None):
        return scooters_controller.get_scooters()


@router.post(
    '/createScooter',
    response_model=GoodResponse,
    dependencies=[Depends(allow_create_requests)],
    status_code=status.HTTP_201_CREATED
)
async def create_scooter(
        scooter: InputScooterName = Body(
            default=InputScooterName(),
            description='Data of a scooter to create.',
            example={
                'scooterName': 'TestScooterModel'
            }
        )
):
    """Create scooter via the provided data."""

    scooters_controller.add_scooter(scooter=scooter)
    return GoodResponse()


@router.put('/bookScooter', response_model=GoodResponse)
async def book_scooter(
        user_id: int = Query(description='The ID of a user who is booking the provided scooter.'),
        scooter_id: int = Query(description='The ID of a booking scooter.')
):
    """Book the provided scooter."""

    if not users_controller.is_user(payload=user_id):
        raise UserDoesNotExist(user_id=user_id)

    if not scooters_controller.is_scooter(scooter_id=scooter_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Scooter does not exist.'
        )

    if not scooters_controller.is_available(scooter_id=scooter_id):
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail='Scooter is not available right now.'
        )

    if scooters_controller.is_booked(scooter_id=scooter_id):
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail='Scooter has already booked.'
        )

    scooters_controller.book_scooter(booking_scooter_id=scooter_id, booking_user_id=user_id)
    return GoodResponse()


@router.put('/unbookScooter', response_model=GoodResponse)
async def unbook_scooter(scooter_id: int = Query(description='Booked scooter\'s identifier to unbook it.')):
    """Unbook the provided scooter."""

    if not scooters_controller.is_scooter(scooter_id=scooter_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Scooter does not exist.'
        )

    if not scooters_controller.is_booked(scooter_id=scooter_id):
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail='Scooter is not booked.'
        )

    scooters_controller.unbook_scooter(booked_scooter_id=scooter_id)
    return GoodResponse()


@router.put('/activateScooter', response_model=GoodResponse)
async def activate_scooter(scooter_id: int = Query(description='The ID of a scooter to activate.')):
    """Activate the provided scooter."""

    if not scooters_controller.is_scooter(scooter_id=scooter_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Scooter does not exist.'
        )

    if scooters_controller.is_available(scooter_id=scooter_id):
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail='Scooter is already activated.'
        )

    scooters_controller.activate_scooter(scooter_id=scooter_id)
    return GoodResponse()


@router.put('/deactivateScooter', response_model=GoodResponse)
async def deactivate_scooter(scooter_id: int = Query(description='The ID of a scooter to deactivate.')):
    """Deactivate the provided scooter."""

    if not scooters_controller.is_scooter(scooter_id=scooter_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Scooter does not exist.'
        )

    if not scooters_controller.is_available(scooter_id=scooter_id):
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail='Scooter is already deactivated.'
        )

    scooters_controller.deactivate_scooter(scooter_id=scooter_id)

    return GoodResponse()


@router.delete(
    '/deleteScooter',
    response_model=GoodResponse,
    dependencies=[Depends(allow_delete_requests)]
)
async def delete_scooter(scooter_id: int = Query(description='Scooter\'s identifier to delete it from database.')):
    """Delete scooter's data from database."""

    if not scooters_controller.is_scooter(scooter_id=scooter_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Scooter does not exist.'
        )
    scooters_controller.delete_scooter(scooter_id=scooter_id)
    return GoodResponse()
