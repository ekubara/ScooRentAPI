from fastapi import Request, status
from fastapi.responses import JSONResponse

from scoorent.exceptions.users import (
    EmailAlreadyInUse, UserAlreadyExists, UserDoesNotExist,
    IncorrectPhoneNumber
)
from scoorent.exceptions.globals import ProvideAnyParameter


async def process_user_already_exists_exc(request: Request, exc: UserAlreadyExists):
    """Process `UserAlreadyExists` exception."""

    return JSONResponse(
        status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
        content={UserAlreadyExists.__name__: UserAlreadyExists(exc.user_id).__str__()}
    )


async def process_user_does_not_exist_exc(request: Request, exc: UserDoesNotExist):
    """Process `UserDoesNotExist` exception."""

    return JSONResponse(
        status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
        content={UserDoesNotExist.__name__: UserDoesNotExist(exc.user_id).__str__()}
    )


async def process_email_is_already_in_use_exc(request: Request, exc: EmailAlreadyInUse):
    """Process `EmailAlreadyInUse` exception."""

    return JSONResponse(
        status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
        content={EmailAlreadyInUse.__name__: EmailAlreadyInUse(exc.email).__str__()}
    )


async def process_incorrect_phone_number_exc(request: Request, exc: IncorrectPhoneNumber):
    """Process `IncorrectPhoneNumber` exception."""

    return JSONResponse(
        status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
        content={IncorrectPhoneNumber.__name__: IncorrectPhoneNumber(exc.phone_number).__str__()}
    )


async def process_no_parameters_provided(request: Request, exc: ProvideAnyParameter):
    """Process `ProvideAnyParameter` exception."""

    return JSONResponse(
        status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
        content={ProvideAnyParameter.__name__: ProvideAnyParameter().__str__()}
    )


exceptions = {
    EmailAlreadyInUse:  process_email_is_already_in_use_exc,
    IncorrectPhoneNumber: process_incorrect_phone_number_exc,
    ProvideAnyParameter: process_no_parameters_provided,
    UserAlreadyExists: process_user_already_exists_exc,
    UserDoesNotExist:  process_user_does_not_exist_exc,
}
