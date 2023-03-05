from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str = Field(alias='accessToken')
    token_type: str = Field(alias='tokenType')

    class Config:
        allow_population_by_field_name = True


class TokenData(BaseModel):
    sub: str
    can_get: bool
    can_create: bool
    can_delete: bool


class Permissions(BaseModel):
    can_get: bool = True
    can_create: bool = True
    can_delete: bool = True
