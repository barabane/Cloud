from passlib.hash import pbkdf2_sha256
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.UserModel import User
from src.database.schemas.UserSchemas import SUserAuth, SUserResponse
from src.exceptions import (
    UserAlreadyExistsException,
    UserBadCredentialsException,
    UserDoesNotExistsException,
)
from src.repositories.UserRepository import UserRepository, get_user_repository
from src.services.BaseService import BaseService


class UserService(BaseService):
    def __init__(self, repository: UserRepository):
        super().__init__(repository=repository)

    async def register(
        self, user_request: SUserAuth, session: AsyncSession
    ) -> SUserResponse:
        user_exists: User | None = await self.repository.get_by_email(
            user_request.email, session
        )

        if user_exists:
            raise UserAlreadyExistsException(
                detail='Пользователь с таким email уже существует'
            )

        hashed_pwd = pbkdf2_sha256.hash(user_request.password)

        user_dict = {'email': user_request.email, 'hashed_password': hashed_pwd}

        user: User = await self.repository.add(user_dict, session)

        return SUserResponse(**user.__dict__)

    async def login(
        self, user_request: SUserAuth, session: AsyncSession
    ) -> SUserResponse:
        user: User | None = await self.repository.get_by_email(
            user_request.email, session
        )

        if not user:
            raise UserDoesNotExistsException(
                detail='Пользователь с таким email не найден'
            )
        is_verified: bool = self.__check_pwd_hash(
            user_request.password, user.hashed_password
        )

        if not is_verified:
            raise UserBadCredentialsException()

        return SUserResponse(**user.__dict__)

    @staticmethod
    def __check_pwd_hash(password: str, hashed_password: str) -> bool:
        return pbkdf2_sha256.verify(password, hashed_password)


def get_user_service() -> UserService:
    return UserService(repository=get_user_repository())
