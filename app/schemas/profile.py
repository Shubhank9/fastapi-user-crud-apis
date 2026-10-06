from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ProfileCreate(BaseModel):
    name: str
    phone: Optional[str] = None
    age: Optional[int] = None
    location: Optional[str] = None
    bio: Optional[str] = None


class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    age: Optional[int] = None
    location: Optional[str] = None
    bio: Optional[str] = None


class ProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # Allows Pydantic to read data directly from SQLAlchemy objects

    id: int
    user_id: int
    name: str
    phone: Optional[str]
    age: Optional[int]
    location: Optional[str]
    bio: Optional[str]
    created_at: datetime
    updated_at: datetime