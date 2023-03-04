from ..model import Connector
from app.types.models import Scooter


class ScootersController(Connector):
    """This class is controller for `Scooters` table."""

    def __init__(self):
        self.cursor = super().connection.cursor(buffered=True)

    @staticmethod
    def _collect_scooter_object(dirty_scooter_data: tuple[...]) -> Scooter:
        """Collect scooter's object."""

        return Scooter(
            id=dirty_scooter_data[0],
            scooter_name=dirty_scooter_data[1],
            is_available=dirty_scooter_data[2],
            is_booked=dirty_scooter_data[3],
            booked_by_user_id=dirty_scooter_data[4],
            booked_at=dirty_scooter_data[5]
        )

    async def get_scooter(self, scooter_id: int) -> Scooter:
        """Return scooter's object by its id."""

        with self.cursor:
            self.cursor.execute('select * from Scooters where ID=%s', (scooter_id,))
            return self._collect_scooter_object(self.cursor.fetchone())

    async def is_available(self, scooter_id: int) -> bool:
        """Return `True` if scooter is available, else `False`."""

        with self.cursor:
            self.cursor.execute('select count(*) from Scooters where ID=%s', (scooter_id,))
            scooter_row = self.cursor.fetchone()
            return True if scooter_row else False

    async def is_booked(self, scooter_id: int) -> bool:
        """Return `True` if scooter is booked by smb, else `False`."""

        with self.cursor:
            self.cursor.execute('select isBooked from Scooters where ID=%s', (scooter_id,))
            is_booked = True if self.cursor.fetchone() else False
            return is_booked

    async def add_scooter(self, scooter_name: str) -> Scooter:
        """Create scooter's row and return its object."""

        with self.cursor:
            self.cursor.execute('insert into Scooters (scooterName) values (%s)', (scooter_name,))
            fetched_scooter = self.cursor.fetchone()
            return self._collect_scooter_object(fetched_scooter)

    async def del_scooter(self, scooter_id: int) -> Scooter:
        """Delete scooter's row from `Scooters` and return its instance."""

        with self.cursor:
            self.cursor.execute('select * from Scooters where ID=%s', (scooter_id,))
            fetched_scooter = self.cursor.fetchone()
            self.cursor.execute('delete from Scooters where ID=%s', (scooter_id,))
            return self._collect_scooter_object(fetched_scooter)
