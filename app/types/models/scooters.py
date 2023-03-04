from datetime import datetime

from pydantic import BaseModel, Field


class Scooter(BaseModel):
    id: int = Field(alias='ID')
    scooter_name: str = Field(default='TestScooterModel', alias='scooterName')
    is_available: bool = Field(default=True, alias='isAvailable')
    is_booked: bool = Field(default=False, alias='isBooked')
    booked_by_user_id: int = Field(alias='bookedByUserID')
    booked_at: datetime = Field(alias='bookedAt')

    class Config:
        allow_population_by_field_name = True
