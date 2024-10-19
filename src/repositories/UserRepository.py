from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.UserModel import User
from src.repositories.BaseRepository import BaseRepository


class UserRepository(BaseRepository):
    model: User = User

    async def get_by_email(self, email: str, session: AsyncSession) -> User | None:
        res = await session.execute(select(self.model).where(self.model.email == email))
        return res.scalar_one_or_none()


def get_user_repository() -> UserRepository:
    return UserRepository()
