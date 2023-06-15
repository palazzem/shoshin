from .__about__ import __version__ as VERSION

_TROUBLESHOOTING_DOCS_URL = f"https://github.com/palazzem/shoshin/wiki/{VERSION}-"


class TroubleshootingExceptionMixin:
    """A mixin class for Shoshin exceptions that provides a standard interface for error messages and codes.
    Codes are used to link specific pages in the Shoshin wiki that provide troubleshooting information for the error.

    Attributes:
        message (str): The error message.
        code (int | None): The error code, if available.
    """

    def __init__(self, message: str, code: int | None = None) -> None:
        """Initializes a new instance of the ShoshinExceptionMixin class.

        Args:
            message (str): The error message.
            code (int | None): The error code, if available.
        """
        self.message = message
        self.code = code

    def __str__(self) -> str:
        """Returns a string representation of the exception.

        Returns:
            str: The error message, with a troubleshooting link if a code is available.
        """
        if self.code is None:
            return self.message
        else:
            return f"{self.message}\n\nTo troubleshoot visit {_TROUBLESHOOTING_DOCS_URL}{self.code}"


class ShoshinException(TroubleshootingExceptionMixin, Exception):
    """A generic exception raised within the Shoshin application."""
