from typing import NamedTuple

from pydantic import BaseModel, Field

from app.types.enumerations.cards import Banks


class Card(BaseModel):
    id: int = Field(alias='ID')
    owner_id: int = Field(alias='ownerID')
    four_last_digits: int = Field(alias='fourLastDigits')

    class Config:
        allow_population_by_field_name = True


class InternalCard(Card):
    card_image_path: str = Field(alias='cardImagePath')
    card_bank_name: str = Field(alias='cardBankName')
    hashed_card_data: str = Field(alias='hashedCardData')


class InputCard(NamedTuple):
    owner_id: int
    card_bank_name: Banks
    card_number: str
    card_date: str
    card_cvv: str
