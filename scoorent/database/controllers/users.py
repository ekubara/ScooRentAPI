from sqlalchemy import delete, select, func

from .. import database_session, save_changes
from ..tables import Cards, Users
from .cards import CardsController
from scoorent.types.enumerations.users import GetUserFilter
from scoorent.types.models.cards import Card, InternalCard
from scoorent.types.models.users import User, InputUser


class UsersController(CardsController):
    """This class is controller for `Users` table."""

    def __init__(self):
        super().__init__()

    @staticmethod
    def _collect_user_data_model(dirty_user_data: tuple) -> User:
        """Return cleaned and collected user data model."""

        return User(**dirty_user_data[0].__dict__)

    def get_user(self, payload: str | int, filter_: GetUserFilter = GetUserFilter.by_user_id) -> User:
        """Return user data by provided filter."""

        filters_and_queries = {
            GetUserFilter.by_email: select(Users).where(Users.email == payload),
            GetUserFilter.by_user_id: select(Users).where(Users.id == payload),
            GetUserFilter.by_phone_number: select(Users).where(Users.phone_number == payload)
        }
        return self._collect_user_data_model(
            dirty_user_data=database_session.execute(filters_and_queries[filter_]).fetchone()
        )

    def get_users(self) -> tuple[User, ...]:
        """Return tuple with all users."""

        return tuple([
            self.get_user(payload=user_id_row[0]) for user_id_row in database_session.execute(select(Users.id))
        ])

    @staticmethod
    def is_user(payload: str | int, filter_: GetUserFilter = GetUserFilter.by_user_id) -> bool:
        """Search user by a filter and return `True` if user exists, `False` otherwise."""

        filters_and_queries = {
            GetUserFilter.by_user_id: select(func.count()).select_from(Users).where(Users.id == payload),
            GetUserFilter.by_email: select(func.count()).select_from(Users).where(Users.email == payload),
            GetUserFilter.by_phone_number: select(func.count()).select_from(Users).where(Users.phone_number == payload)
        }
        return bool(database_session.execute(filters_and_queries[filter_]).fetchone()[0])

    def create_user(self, user: InputUser) -> User:
        """Create user and return its row data."""

        new_user = Users(
            phone_number=user.phone_number,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email
        )
        save_changes(entity=new_user)
        return self.get_user(
            payload=database_session.execute(
                select(Users.phone_number).where(Users.phone_number == user.phone_number)
            ), filter_=GetUserFilter.by_phone_number
        )

    @staticmethod
    def delete_user(user_id: int) -> None:
        """Delete user from `Users` table."""

        database_session.execute(delete(Users).where(Users.id == user_id))
        save_changes()

    def get_user_cards(
            self,
            owner_id: int,
            get_internal: bool = False
    ) -> tuple[Card, ...] | tuple[InternalCard, ...]:
        """Return tuple with all user's cards models.
        Set `get_internal=True` to get tuple of `InternalCard` models."""

        dirty_cards = database_session.execute(select(Cards).where(Cards.owner_id == owner_id)).fetchall()
        return tuple([
            super()._collect_card_data_model(
                dirty_card_data=dirty_card_data,
                get_internal=get_internal
            ) for dirty_card_data in dirty_cards
        ])


users_controller = UsersController()
