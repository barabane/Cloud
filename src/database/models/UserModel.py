import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from src.database.database import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(VARCHAR, nullable=False, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(VARCHAR, nullable=False)
    subscription_id: Mapped[int] = mapped_column(
        ForeignKey('subscriptions.id'), nullable=False
    )
