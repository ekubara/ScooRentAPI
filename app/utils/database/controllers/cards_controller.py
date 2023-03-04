from ..model import Connector

from app.types.models import Card, InternalCard, InputCard


class CardsController(Connector):
    """Controller for `Cards` table."""

    def __init__(self):
        self.cursor = super().connection.cursor(buffered=True)

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

        pass

    def delete_card(self, last_four_digits: int, owner_id: int) -> bool:
        """Delete card from database."""

        pass


cards_controller = CardsController()
