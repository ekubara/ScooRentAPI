from typing import Any

from .cards_controller import CardsController
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

        return User(
            id=dirty_user_data[0],
            phone_number=dirty_user_data[1],
            first_name=dirty_user_data[2],
            last_name=dirty_user_data[3],
            email=dirty_user_data[4],
            registration_date=dirty_user_data[5]
        )

    def get_user(self, payload: str | int, filter_: GetUserFilter = GetUserFilter.by_user_id):
        """Return user searched by provided filter."""

        filters_and_queries = {
            GetUserFilter.by_email: 'select * from Users where email=%s',
            GetUserFilter.by_user_id: 'select * from Users where ID=%s',
            GetUserFilter.by_phone_number: 'select * from Users where phoneNumber=%s'
        }

        with super().connection.cursor(buffered=True) as cursor:
            cursor.execute(filters_and_queries[filter_], (payload,))
            dirty_user_data = cursor.fetchone()
            return self._collect_user_data_model(dirty_user_data)

    def get_users(self) -> tuple[User, ...]:
        """Return tuple with all users."""

        with super().connection.cursor(buffered=True) as cursor:
            cursor.execute('select ID from Users')
            return tuple([
                self.get_user(payload=user_id_row[0]) for user_id_row in cursor.fetchall()
            ])

    def is_user(self, payload: Any, filter_: GetUserFilter = GetUserFilter.by_user_id) -> bool:
        """Search user by a filter and return `True` if user exists, `False` otherwise."""

        filters_and_queries = {
            GetUserFilter.by_user_id: 'select count(*) from Users where ID=%s',
            GetUserFilter.by_email: 'select count(*) from Users where email=%s',
            GetUserFilter.by_phone_number: 'select count(*) from Users where phoneNumber=%s'
        }

        with super().connection.cursor(buffered=True) as cursor:
            cursor.execute(filters_and_queries[filter_], (payload,))
            return bool(cursor.fetchone()[0])

    def create_user(self, user: InputUser) -> User:
        """Create user and return its row data."""

        with super().connection.cursor(buffered=True) as cursor:
            cursor.execute(
                'insert into Users (phoneNumber, firstName, lastName, email) '
                'values (%s, %s, %s, %s)',
                (user.phone_number, user.first_name, user.last_name, user.email)
            )
            cursor.execute('select ID from Users where phoneNumber=%s', (user.phone_number,))
            return self.get_user(payload=cursor.fetchone()[0])

    def delete_user(self, user_id: int) -> None:
        """Delete user from `Users` table."""

        with super().connection.cursor(buffered=True) as cursor:
            cursor.execute('delete from Users where ID=%s', (user_id,))

    def get_user_cards(
            self,
            owner_id: int,
            get_internal: bool = False
    ) -> tuple[Card, ...] | tuple[InternalCard, ...]:
        """Return tuple with all user's cards models.
        Set `get_internal=True` to get tuple of `InternalCard` models."""

        with super().connection.cursor(buffered=True) as cursor:
            cursor.execute('select * from Cards where ownerID=%s', (owner_id,))
            dirty_cards = cursor.fetchall()
            return tuple([
                super()._collect_card_data_model(
                    dirty_card_data=dirty_card_data,
                    get_internal=get_internal
                ) for dirty_card_data in dirty_cards
            ])


users_controller = UsersController()
