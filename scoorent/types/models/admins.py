from datetime import datetime

from pydantic import BaseModel, Field


class Admin(BaseModel):
    id: int = Field(alias='ID')
    username: str
    can_get: bool = Field(default=True, alias='canGet')
    can_create: bool = Field(default=True, alias='canCreate')
    can_edit: bool = Field(default=True, alias='canEdit')
    can_delete: bool = Field(default=True, alias='canDelete')
    registration_date: datetime = Field(alias='registrationDate')

    class Config:
        allow_population_by_field_name = True


class InternalAdmin(Admin):
    password: str
