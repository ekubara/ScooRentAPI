class UserDoesNotExist(Exception):
    """Raises if requested user does not seem to exist."""

    def __init__(self, user_id: int):
        self.user_id = user_id

    def __str__(self):
        return f"User #{self.user_id} doesn't exist."


class UserAlreadyExists(Exception):
    """Raises while trying to create user that already existed."""

    def __init__(self, user_id: int):
        self.user_id = user_id

    def __str__(self):
        return f"User #{self.user_id} already exists."


class EmailAlreadyInUse(Exception):
    """Raises while trying to use registered email."""

    def __init__(self, email: str):
        self.email = email

    def __str__(self):
        return f"Email {self.email} is already in use."


class IncorrectPhoneNumber(Exception):
    """Raises while trying to register incorrect phone number."""

    def __init__(self, phone_number: str):
        self.phone_number = phone_number

    def __str__(self):
        return f"Phone number '{self.phone_number}' is incorrect."


class ProvideAnyParameter(Exception):
    """Raises if dev called `get user` function without any parameter."""

    def __str__(self):
        return "Provide at least 1 parameter."
