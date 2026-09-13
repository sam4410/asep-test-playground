from datetime import date
from typing import List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field, validator


def validate_weekdays(value: List[int]) -> List[int]:
    if not value:
        raise ValueError("at least one weekday is required")
    if len(value) != len(set(value)):
        raise ValueError("weekdays must not contain duplicates")
    if any(day < 0 or day > 6 for day in value):
        raise ValueError("weekdays must contain values from 0 through 6")
    return sorted(value)


class HabitBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    weekdays: List[int] = Field(default_factory=lambda: list(range(7)))

    @validator("name")
    def name_must_not_be_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("name must not be blank")
        return value

    @validator("weekdays")
    def weekdays_must_be_valid(cls, value: List[int]) -> List[int]:
        return validate_weekdays(value)


class HabitCreate(HabitBase):
    template_key: Optional[str] = Field(default=None, max_length=100)


class HabitUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    weekdays: Optional[List[int]] = None

    @validator("name")
    def name_must_not_be_blank(cls, value: Optional[str]) -> Optional[str]:
        if value is not None:
            value = value.strip()
            if not value:
                raise ValueError("name must not be blank")
        return value

    @validator("weekdays")
    def weekdays_must_be_valid(
        cls, value: Optional[List[int]]
    ) -> Optional[List[int]]:
        return None if value is None else validate_weekdays(value)


class Habit(HabitBase):
    id: str = Field(default_factory=lambda: str(uuid4()))
    template_key: Optional[str] = None
    predefined: bool = False


class CompletionLog(BaseModel):
    local_today: date = Field(default_factory=date.today)
    completion_date: date
    completed: bool = True

    @validator("local_today")
    def local_today_must_not_be_in_the_future(cls, value: date) -> date:
        if value > date.today():
            raise ValueError("local_today cannot be in the future")
        return value

    @validator("completion_date")
    def completion_must_be_today(cls, value: date, values) -> date:
        local_today = values.get("local_today")
        if local_today is not None and value != local_today:
            raise ValueError("habit completions can only be logged for today")
        return value


class StreakCalculationRequest(BaseModel):
    completed_dates: List[date] = Field(default_factory=list)
    weekdays: List[int] = Field(default_factory=lambda: list(range(7)))
    through: date = Field(default_factory=date.today)

    @validator("weekdays")
    def weekdays_must_be_valid(cls, value: List[int]) -> List[int]:
        return validate_weekdays(value)

    @validator("through")
    def through_must_not_be_in_the_future(cls, value: date) -> date:
        if value > date.today():
            raise ValueError("through cannot be in the future")
        return value


class StreakResult(BaseModel):
    current_streak: int
    longest_streak: int


class CompletionResult(BaseModel):
    habit_id: str
    completion_date: date
    completed: bool
