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
