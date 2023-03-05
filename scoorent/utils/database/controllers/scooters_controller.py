from datetime import datetime

from ..model import Connector
from scoorent.types.models import Scooter, InputScooterName


class ScootersController(Connector):
    """This class is controller for `Scooters` table."""

    @staticmethod
    def _collect_scooter_object(dirty_scooter_data: tuple) -> Scooter:
        """Collect scooter's object."""

        return Scooter(
            id=dirty_scooter_data[0],
            scooter_name=dirty_scooter_data[1],
            is_available=dirty_scooter_data[2],
            is_booked=dirty_scooter_data[3],
            booked_by_user_id=dirty_scooter_data[4],
            booked_at=dirty_scooter_data[5]
        )

    def get_scooter(self, scooter_id: int) -> Scooter:
        """Return scooter's object by its id."""

        with super().connection.cursor(buffered=True) as cursor:
            cursor.execute('select * from Scooters where ID=%s', (scooter_id,))
            return self._collect_scooter_object(cursor.fetchone())

    def get_scooters(self) -> tuple[Scooter, ...]:
        """Return tuple with all scooters database has."""

        with super().connection.cursor(buffered=True) as cursor:
            cursor.execute('select ID from Scooters')
            return tuple([
                self.get_scooter(
                    scooter_id=scooter_id_row[0]
                ) for scooter_id_row in cursor.fetchall()
            ])

    def is_scooter(self, scooter_id: int) -> bool:
        """Return `True` if scooter exists, otherwise `False`."""

        with super().connection.cursor(buffered=True) as cursor:
            cursor.execute('select count(*) from Scooters where ID=%s', (scooter_id,))
            return bool(cursor.fetchone()[0])

    def is_available(self, scooter_id: int) -> bool:
        """Return `True` if scooter is available, else `False`."""

        with super().connection.cursor(buffered=True) as cursor:
            cursor.execute('select isAvailable from Scooters where ID=%s', (scooter_id,))
            return True if cursor.fetchone()[0] else False

    def is_booked(self, scooter_id: int) -> bool:
        """Return `True` if scooter is booked by smb, else `False`."""

        with super().connection.cursor(buffered=True) as cursor:
            cursor.execute('select isBooked from Scooters where ID=%s', (scooter_id,))
            return True if cursor.fetchone()[0] else False

    def book_scooter(self, booking_scooter_id: int, booking_user_id: int) -> None:
        """Change scooter's data to book it."""

        with super().connection.cursor(buffered=True) as cursor:
            cursor.execute(
                'update Scooters set isBooked=true, bookedByUserID=%s, bookedAtDate=%s where ID=%s',
                (booking_user_id, datetime.now(), booking_scooter_id)
            )

    def unbook_scooter(self, booked_scooter_id: int) -> None:
        """Change scooter's data to unbook it."""

        with super().connection.cursor(buffered=True) as cursor:
            cursor.execute(
                'update Scooters set isBooked=false, bookedByUserID=NULL, bookedAtDate=NULL where ID=%s',
                (booked_scooter_id,)
            )

    def activate_scooter(self, scooter_id: int) -> None:
        """Activate scooter."""

        with super().connection.cursor(buffered=True) as cursor:
            cursor.execute('update Scooters set isAvailable=true where ID=%s', (scooter_id,))

    def deactivate_scooter(self, scooter_id: int) -> None:
        """Deactivate scooter."""

        with super().connection.cursor(buffered=True) as cursor:
            cursor.execute('update Scooters set isAvailable=false where ID=%s', (scooter_id,))

    def add_scooter(self, scooter: InputScooterName) -> None:
        """Create scooter's row and return its object."""

        with super().connection.cursor(buffered=True) as cursor:
            cursor.execute('insert into Scooters (scooterName) values (%s)', (scooter.scooter_name,))

    def delete_scooter(self, scooter_id: int) -> Scooter:
        """Delete scooter's row from `Scooters` and return its instance."""

        with super().connection.cursor(buffered=True) as cursor:
            cursor.execute('select * from Scooters where ID=%s', (scooter_id,))
            fetched_scooter = cursor.fetchone()
            cursor.execute('delete from Scooters where ID=%s', (scooter_id,))
            return self._collect_scooter_object(fetched_scooter)


scooters_controller = ScootersController()
