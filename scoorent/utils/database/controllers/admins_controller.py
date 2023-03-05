from ..model import Connector
from scoorent.types.enumerations.admins import GetAdminFilter
from scoorent.types.models.admins import Admin, InternalAdmin
from scoorent.middlewares.security import hash_entity


class AdminsController(Connector):
    """Admins table controller."""

    @staticmethod
    def _collect_admin_model(dirty_admin_data: tuple) -> Admin:
        """Clean and return admin's model."""

        return Admin(
            id=dirty_admin_data[0],
            username=dirty_admin_data[1],
            can_get=dirty_admin_data[3],
            can_create=dirty_admin_data[4],
            can_delete=dirty_admin_data[5],
            registration_date=dirty_admin_data[6]
        )

    def collect_internal_admin_model(self, username: str) -> InternalAdmin:
        """Return internal admin's model."""

        with super().connection.cursor(buffered=True) as cursor:
            cursor.execute('select password from Admins where username=%s', (username,))
            admin_password = cursor.fetchone()[0]
            public_admin_model = self.get_admin(payload=username, filter_=GetAdminFilter.by_username)
            return InternalAdmin(**public_admin_model.dict(), password=admin_password)

    def get_admin(self, payload: str, filter_: GetAdminFilter = GetAdminFilter.by_id) -> Admin | bool:
        """Return admin's model."""

        filters_and_queries = {
            GetAdminFilter.by_id: 'select * from Admins where ID=%s',
            GetAdminFilter.by_username: 'select * from Admins where username=%s'
        }

        with super().connection.cursor(buffered=True) as cursor:
            cursor.execute(filters_and_queries[filter_], (payload,))
            admin_data = cursor.fetchone()
            if not admin_data:
                return False
            return self._collect_admin_model(admin_data)

    def is_existing_admin(
            self, payload: str | int,
            filter_: GetAdminFilter = GetAdminFilter.by_username
    ) -> bool:
        """Return `True` if admins exists, `False` otherwise."""

        if not self.get_admin(payload=payload, filter_=filter_):
            return False
        return True

    def create_admin(self, username: str, password: str) -> Admin:
        """Create admin and return its data model."""

        hashed_password = hash_entity(password)

        with super().connection.cursor(buffered=True) as cursor:
            cursor.execute('insert into Admins (username, password) values (%s, %s)', (username, hashed_password))
            return self.get_admin(payload=username, filter_=GetAdminFilter.by_username)

    def delete_admin(self, admin_id: int):
        """Delete admin's data from database."""

        with super().connection.cursor(buffered=True) as cursor:
            cursor.execute('delete from Admins where ID=%s', (admin_id,))


admins_controller = AdminsController()
