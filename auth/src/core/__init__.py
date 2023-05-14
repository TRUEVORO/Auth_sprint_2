from .exceptions import (
    AuthError,
    EmptyRequestError,
    NoPermissionError,
    UserExistError,
    UserNotExistError,
    WrongPasswordError,
)
from .settings import Settings, settings

__all__ = (
    'AuthError',
    'UserExistError',
    'UserNotExistError',
    'WrongPasswordError',
    'NoPermissionError',
    'EmptyRequestError',
    'settings',
    'Settings',
)
