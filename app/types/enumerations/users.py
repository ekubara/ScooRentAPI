from enum import Enum


class GetUserFilter(str, Enum):
    by_email = "email_searching_filter"
    by_user_id = "user_id_searching_filter"
    by_phone_number = "phone_number_searching_filter"
