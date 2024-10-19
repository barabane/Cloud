from sqlalchemy.dialects.postgresql import INTEGER, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from src.database.database import Base


class Subscription(Base):
    __tablename__ = 'subscriptions'

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, default=1)
    title: Mapped[str] = mapped_column(VARCHAR, nullable=False)
