from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


class SUser(BaseModel):
    id: UUID
    email: EmailStr
    subscription_id: int


class SUserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    subscription_id: Optional[int] = None


class SUserResponse(BaseModel):
    id: UUID | str
    email: EmailStr
    subscription_id: Optional[int] = None


class SUserAuth(BaseModel):
    email: EmailStr
    password: str
