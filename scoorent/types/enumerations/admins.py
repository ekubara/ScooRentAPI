from enum import Enum


class GetAdminFilter(str, Enum):
    by_id = "get_admin_by_id"
    by_username = "get_admin_by_username"
