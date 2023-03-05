class ProvideAnyParameter(Exception):
    """Raises while trying to use some method (that needs some value
    to be passed to it) without providing any parameter."""

    def __str__(self):
        return "Provide at least 1 parameter."
