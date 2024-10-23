from typing import Any

from fastapi import HTTPException, status


class DefaultException(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail: Any = None,
    ):
        super().__init__(status_code=status_code, detail=detail)


class UserAlreadyExistsException(DefaultException):
    def __init__(
        self,
        status_code: int = status.HTTP_409_CONFLICT,
        detail: Any = 'Пользователь уже существует',
    ):
        super().__init__(status_code, detail)


class UserDoesNotExistsException(DefaultException):
    def __init__(
        self,
        status_code: int = status.HTTP_404_NOT_FOUND,
        detail: Any = 'Пользователь не найден',
    ):
        super().__init__(status_code, detail)


class UserBadCredentialsException(DefaultException):
    def __init__(
        self,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        detail: Any = 'Неправильный логин или пароль',
    ):
        super().__init__(status_code, detail)


class TokenNotFoundException(DefaultException):
    def __init__(
        self,
        status_code: int = status.HTTP_404_NOT_FOUND,
        detail: Any = 'Auth token не найден',
    ):
        super().__init__(status_code, detail)


class TokenExpiredException(DefaultException):
    def __init__(
        self,
        status_code: int = status.HTTP_401_UNAUTHORIZED,
        detail: Any = 'Auth token истек',
    ):
        super().__init__(status_code, detail)


class InvalidTokenException(DefaultException):
    def __init__(
        self,
        status_code: int = status.HTTP_401_UNAUTHORIZED,
        detail: Any = 'Не валидный Auth token',
    ):
        super().__init__(status_code, detail)
