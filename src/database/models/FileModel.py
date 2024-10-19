import uuid
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import FLOAT, TIMESTAMP, UUID, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from src.database.database import Base
from src.database.models import BaseModel


class File(BaseModel, Base):
    __tablename__ = 'files'

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(VARCHAR, nullable=False)
    size: Mapped[float] = mapped_column(FLOAT, nullable=False, default=0.0)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False, default=datetime.now
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False, default=datetime.now
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID, ForeignKey('users.id'), nullable=False
    )
