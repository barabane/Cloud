from fastapi import Request
from jwt import PyJWTError
from starlette.middleware.base import BaseHTTPMiddleware

from src.exceptions import InvalidTokenException, TokenNotFoundException
from src.utils.TokenService import TokenService


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, prefixes) -> None:
        super().__init__(app)

        self.prefixes = prefixes

    async def dispatch(self, request: Request, call_next):
        if not any(request.url.path.startswith(prefix) for prefix in self.prefixes):
            response = await call_next(request)
            return response

        auth_token = request.cookies.get('auth_token')

        if not auth_token:
            raise TokenNotFoundException()

        try:
            payload = TokenService.decode_token(token=auth_token)
            request.state.user = payload
        except PyJWTError:
            raise InvalidTokenException()

        response = await call_next(request)
        return response
