def is_phone_number(phone_number: str) -> bool:
    """Return `True` if user's phone number is valid, `False` otherwise."""

    phone_number = phone_number.strip('+')

    if (
            (phone_number[0] == '7') or
            (phone_number[0] == '8')
    ):
        if prettify_phone_number(phone_number).replace('+7', '').__len__() == 10:
            return True
    return False


def prettify_phone_number(ugly_phone_number: str) -> str:
    """Prettify user's phone number."""

    ugly_phone_number = ugly_phone_number.strip('+')
    ugly_phone_number = ugly_phone_number.replace(' ', '')

    if (ugly_phone_number[0] == '7') or (ugly_phone_number[0] == '8'):
        pretty_phone_number = f"+7{ugly_phone_number[1:]}"
        return pretty_phone_number
