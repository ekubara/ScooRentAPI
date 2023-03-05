from datetime import datetime

from pydantic import BaseModel, Field


class Scooter(BaseModel):
    id: int = Field(alias='ID')
    scooter_name: str = Field(default='TestScooterModel', alias='scooterName', min_length=1, max_length=100)
    is_available: bool = Field(default=True, alias='isAvailable')
    is_booked: bool = Field(default=False, alias='isBooked')
    booked_by_user_id: int = Field(default=None, alias='bookedByUserID')
    booked_at: datetime | None = Field(default=None, alias='bookedAt')

    class Config:
        allow_population_by_field_name = True


class InputScooterName(BaseModel):
    scooter_name: str = Field(default='TestScooterModel', min_length=1, max_length=100)

    class Config:
        allow_population_by_field_name = True


class InputScooterID(BaseModel):
    scooter_id: int

    class Config:
        allow_population_by_field_name = True
