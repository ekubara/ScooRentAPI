from sqlalchemy import and_, select, delete

from .. import database_session, save_changes
from ..tables import Cards
from scoorent.middlewares.security import hash_entity
from scoorent.types.models.cards import Card, InternalCard, InputCard


class CardsController:
    """Controller for `Cards` table."""

    @staticmethod
    def _collect_card_data_model(dirty_card_data: tuple, get_internal: bool = False) -> Card | InternalCard:
        """Return collected card data model.
        Set `get_internal=True` to get `InternalCard` instead of normal `Card` data model."""

        internal_card_data_model = InternalCard(**dirty_card_data[0].__dict__)

        if get_internal:
            return internal_card_data_model
        return Card(
            id=internal_card_data_model.id,
            owner_id=internal_card_data_model.owner_id,
            four_last_digits=internal_card_data_model.four_last_digits,
        )

    def add_card(self, card: InputCard) -> InternalCard:
        """Create new card row in database."""

        card.card_number = card.card_number.replace(' ', '')
        four_last_digits = card.card_number[-4:]
        hashed_card_data = hash_entity(f'{card.card_number}|{card.card_date}|{card.card_cvv}')

        new_card = Cards(
            owner_id=card.owner_id,
            card_image_path=f'image://{card.card_bank_name.value}',
            card_bank_name=card.card_bank_name.value,
            hashed_card_data=hashed_card_data,
            four_last_digits=int(four_last_digits)
        )
        save_changes(new_card)
        return self._collect_card_data_model(
            dirty_card_data=database_session.execute(
                select(Cards)
                .where(
                    and_(
                        Cards.owner_id == card.owner_id,
                        Cards.four_last_digits == four_last_digits
                    )
                )
            ).fetchone(),
            get_internal=True
        )

    @staticmethod
    def delete_card(four_last_digits: int, owner_id: int) -> bool:
        """Delete card from database."""

        database_session.execute(
            delete(Cards)
            .where(
                and_(
                    Cards.owner_id == owner_id,
                    Cards.four_last_digits == four_last_digits
                )
            )
        )
        save_changes()
        return True


cards_controller = CardsController()
