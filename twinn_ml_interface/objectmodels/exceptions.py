from dataclasses import dataclass
from enum import Enum
from typing import Protocol, runtime_checkable


class MessageType(Enum):
    INTERNAL_MESSAGE_TEXT = "InternalErrorMessage"
    CLIENT_MESSAGE_TEXT = "ClientErrorMessage"


class InfoTagLevel(str, Enum):
    INFO = "information"
    WARN = "warning"
    ERROR = "error"


@dataclass
class InfoTag:
    level: InfoTagLevel
    tag: str


@dataclass
class ErrorMessages:
    traceback: str
    internal_error_message: str
    client_error_message: str | None = None
    exception_type: str | None = None


@runtime_checkable
class BaseError(Protocol):
    INTERNAL_MESSAGE: str = None
    CLIENT_MESSAGE: str = None


def construct_model_exception_text(internaL_message: str, client_message: str) -> str:
    """Build a parsable log string

    Parameters
    ----------
    internaL_message : str
        The internal message to add to the log
    client_message : str
        The client message to add to the log

    Returns
    -------
    str
        A parsable log string containing the internal message and client message
    """
    return (
        f"{MessageType.INTERNAL_MESSAGE_TEXT.value}: {internaL_message}\n"
        f"{MessageType.CLIENT_MESSAGE_TEXT.value}: {client_message}"
    )


class ModelException(Exception):
    """
    Custom Exception that allows the use of BaseError
    """

    def __init__(self, error_code: BaseError):
        """
        Parameters
        ----------
        error_code : BaseError
            The desired error we want to raise
        """
        self.error_code = error_code
        super().__init__(self.error_code.INTERNAL_MESSAGE)

    def __str__(self):
        msg = construct_model_exception_text(
            self.error_code.INTERNAL_MESSAGE, self.error_code.CLIENT_MESSAGE
        )
        return msg
