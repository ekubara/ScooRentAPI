from ..model import Connector

from scoorent.middlewares.security import hash_entity
from scoorent.types.models.cards import Card, InternalCard, InputCard


class CardsController(Connector):
    """Controller for `Cards` table."""

    @staticmethod
    def _collect_card_data_model(dirty_card_data: tuple, get_internal: bool = False) -> Card | InternalCard:
        """Return collected card data model.
        Set `get_internal=True` to get `InternalCard` instead of normal `Card` data model."""

        internal_card_data_model = InternalCard(
            id=dirty_card_data[0],
            owner_id=dirty_card_data[1],
            card_image_path=dirty_card_data[2],
            card_bank_name=dirty_card_data[3],
            hashed_card_data=dirty_card_data[4],
            four_last_digits=dirty_card_data[5],
        )

        if get_internal:
            return internal_card_data_model
        return Card(
            id=internal_card_data_model.id,
            owner_id=internal_card_data_model.owner_id,
            four_last_digits=internal_card_data_model.four_last_digits,
        )

    def add_card(self, card: InputCard) -> InternalCard:
        """Add and return card data model."""

        card.card_number = card.card_number.replace(' ', '')
        four_last_digits = card.card_number[-4:]
        hashed_card_data = hash_entity(f'{card.card_number}|{card.card_date}|{card.card_cvv}')

        with super().connection.cursor(buffered=True) as cursor:
            cursor.execute(
                'insert into Cards ('
                'ownerID, cardImagePath, cardBankName, hashedCardData, fourLastDigits'
                ') values (%s, %s, %s, %s, %s)',
                (
                    card.owner_id,
                    f'image://{card.card_bank_name.value}',
                    card.card_bank_name.value,
                    hashed_card_data,
                    four_last_digits
                )
            )
            cursor.execute(
                'select * from Cards where ownerID=%s and fourLastDigits=%s',
                (card.owner_id, four_last_digits)
            )
            return self._collect_card_data_model(dirty_card_data=cursor.fetchone(), get_internal=True)

    def delete_card(self, four_last_digits: int, owner_id: int) -> bool:
        """Delete card from database."""

        with super().connection.cursor(buffered=True) as cursor:
            cursor.execute(
                'delete from Cards where ownerID=%s and fourLastDigits=%s',
                (owner_id, four_last_digits)
            )
            return True


cards_controller = CardsController()
