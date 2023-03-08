from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    """User's pydantic model."""

    id: int = Field(alias='ID')
    phone_number: str = Field(alias='phoneNumber')
    first_name: str = Field(alias='firstName')
    last_name: str = Field(alias='lastName')
    email: EmailStr
    registration_date: datetime = Field(alias='registrationDate')

    class Config:
        allow_population_by_field_name = True


class InputUser(BaseModel):
    """Input user's model."""

    phone_number: str = Field(alias='phoneNumber')
    first_name: str = Field(alias='firstName')
    last_name: str = Field(alias='lastName')
    email: EmailStr

    class Config:
        allow_population_by_field_name = True
