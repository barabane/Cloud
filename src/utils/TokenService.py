from datetime import datetime, timedelta, timezone

import jwt

from src.config import settings


class TokenService:
    @staticmethod
    def create_token(payload: dict) -> str:
        payload['exp'] = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        return jwt.encode(
            payload, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )
