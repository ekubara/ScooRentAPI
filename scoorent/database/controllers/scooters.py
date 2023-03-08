from datetime import datetime

from sqlalchemy import update, select, delete, func

from .. import database_session, save_changes
from ..tables import Scooters
from scoorent.types.models import Scooter, InputScooterName


class ScootersController:
    """This class is controller for `Scooters` table."""

    @staticmethod
    def _collect_scooter_object(dirty_scooter_data: tuple) -> Scooter:
        """Collect scooter's object."""

        return Scooter(**dirty_scooter_data[0].__dict__)

    def get_scooter(self, scooter_id: int) -> Scooter:
        """Return scooter's object by its id."""

        return self._collect_scooter_object(
            dirty_scooter_data=database_session.execute(
                select(Scooters)
                .where(Scooters.id == scooter_id)
            ).fetchone()
        )

    def get_scooters(self) -> tuple[Scooter, ...]:
        """Return tuple with all scooters database has."""

        return tuple([
            self.get_scooter(
                scooter_id=scooter_id_row[0]
            ) for scooter_id_row in database_session.execute(select(Scooters.id))
        ])

    @staticmethod
    def is_scooter(scooter_id: int) -> bool:
        """Return `True` if scooter exists, otherwise `False`."""

        return bool(database_session.execute(
            select(func.count()).select_from(Scooters).where(Scooters.id == scooter_id)
        ).fetchone()[0])

    @staticmethod
    def is_available(scooter_id: int) -> bool:
        """Return `True` if scooter is available, else `False`."""

        return True if database_session.execute(
            select(Scooters.is_available).where(Scooters.id == scooter_id)
        ).fetchone()[0] else False

    @staticmethod
    def is_booked(scooter_id: int) -> bool:
        """Return `True` if scooter is booked by smb, else `False`."""

        return True if database_session.execute(
            select(Scooters.is_booked).where(Scooters.id == scooter_id)
        ).fetchone()[0] else False

    @staticmethod
    def book_scooter(booking_scooter_id: int, booking_user_id: int) -> None:
        """Change scooter's data to book it."""

        database_session.execute(
            update(Scooters)
            .where(Scooters.id == booking_scooter_id)
            .values(is_booked=True, booked_by_user_id=booking_user_id, booked_at_date=datetime.now())
        )
        save_changes()

    @staticmethod
    def unbook_scooter(booked_scooter_id: int) -> None:
        """Change scooter's data to unbook it."""

        database_session.execute(
            update(Scooters)
            .where(Scooters.id == booked_scooter_id)
            .values(is_booked=False, booked_by_user_id=None, booked_at_date=None)
        )
        save_changes()

    @staticmethod
    def activate_scooter(scooter_id: int) -> None:
        """Activate scooter."""

        database_session.execute(
            update(Scooters)
            .where(Scooters.id == scooter_id)
            .values(is_available=True)
        )
        save_changes()

    @staticmethod
    def deactivate_scooter(scooter_id: int) -> None:
        """Deactivate scooter."""

        database_session.execute(
            update(Scooters)
            .where(Scooters.id == scooter_id)
            .values(is_available=False)
        )
        save_changes()

    @staticmethod
    def add_scooter(scooter: InputScooterName) -> None:
        """Create scooter's row and return its object."""

        new_scooter = Scooters(scooter_name=scooter.scooter_name)
        save_changes(new_scooter)

    @staticmethod
    def delete_scooter(scooter_id: int) -> None:
        """Delete scooter's row from `Scooters` and return its instance."""

        database_session.execute(delete(Scooters).where(Scooters.id == scooter_id))
        save_changes()


scooters_controller = ScootersController()
