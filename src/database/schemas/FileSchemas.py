from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class SFile(BaseModel):
    id: UUID
    name: str
    size: float
    created_at: datetime
    updated_at: datetime
    user_id: UUID


class SFileResponse(BaseModel):
    id: UUID
    name: str
    size: float
    created_at: datetime
    updated_at: datetime
    user_id: UUID


class SFileCreate(BaseModel):
    name: str
    size: float
    user_id: UUID


class SFileUpdate(BaseModel):
    name: Optional[str] = None
    size: Optional[float] = None
    user_id: Optional[UUID] = None
