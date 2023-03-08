from sqlalchemy import select, delete

from .. import database_session, save_changes
from ..tables import Admins
from scoorent.types.enumerations.admins import GetAdminFilter
from scoorent.types.models.admins import Admin, InternalAdmin
from scoorent.middlewares.security import hash_entity


class AdminsController:
    """Admins table controller."""

    @staticmethod
    def _collect_admin_model(dirty_admin_data: tuple) -> Admin:
        """Clean and return admin's model."""

        return Admin(**dirty_admin_data[0].__dict__)

    def collect_internal_admin_model(self, username: str) -> InternalAdmin:
        """Return internal admin's model."""

        admin_password = database_session.execute(
            select(Admins.password).where(Admins.username == username)
        ).fetchone()[0]
        public_admin_model = self.get_admin(payload=username, filter_=GetAdminFilter.by_username)
        return InternalAdmin(**public_admin_model.dict(), password=admin_password)

    def get_admin(self, payload: str, filter_: GetAdminFilter = GetAdminFilter.by_id) -> Admin | bool:
        """Return admin's model."""

        filters_and_queries = {
            GetAdminFilter.by_id: select(Admins).where(Admins.id == payload),
            GetAdminFilter.by_username: select(Admins).where(Admins.username == payload)
        }

        dirty_admin_data = database_session.execute(
            filters_and_queries[filter_]
        ).fetchone()
        if not dirty_admin_data:
            return False
        return self._collect_admin_model(dirty_admin_data=dirty_admin_data)

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
        new_admin = Admins(
            username=username,
            password=hashed_password
        )
        save_changes(new_admin)
        return self.get_admin(payload=username, filter_=GetAdminFilter.by_username)

    @staticmethod
    def delete_admin(admin_id: int):
        """Delete admin's data from database."""

        database_session.execute(
            delete(Admins).where(Admins.id == admin_id)
        )
        save_changes()


admins_controller = AdminsController()
