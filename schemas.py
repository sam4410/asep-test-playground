import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class HabitBase(BaseModel):
    name: str
    target_frequency: int = Field(default=7, ge=1, le=7)


class HabitCreate(HabitBase):
    pass


class HabitUpdate(BaseModel):
    name: Optional[str] = None
    target_frequency: Optional[int] = Field(default=None, ge=1, le=7)


class HabitOut(HabitBase):
    id: int
    owner_id: int
    created_at: Optional[datetime.datetime] = None
    current_streak: Optional[int] = 0

    class Config:
        orm_mode = True
        from_attributes = True


class CheckoffCreate(BaseModel):
    date: Optional[datetime.date] = None


class CheckoffOut(BaseModel):
    id: int
    habit_id: int
    date: datetime.date

    class Config:
        orm_mode = True
        from_attributes = True