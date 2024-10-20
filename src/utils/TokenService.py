from datetime import datetime, timedelta, timezone

import jwt

from src.config import settings
from src.exceptions import InvalidTokenException, TokenExpiredException


class TokenService:
    @staticmethod
    def create_token(payload: dict) -> str:
        payload.update(
            {
                'exp': datetime.now(timezone.utc)
                + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            }
        )
        return jwt.encode(
            payload, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )

    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            payload = jwt.decode(
                token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            expire_time = datetime.fromtimestamp(payload['exp']).replace(
                tzinfo=timezone.utc
            )

            if expire_time < datetime.now(timezone.utc):
                raise TokenExpiredException()

            return payload
        except jwt.ExpiredSignatureError:
            raise TokenExpiredException()
        except jwt.DecodeError:
            raise InvalidTokenException()
