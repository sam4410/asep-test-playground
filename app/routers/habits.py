from fastapi import APIRouter, HTTPException, Response, status

from app.schemas.habits import (
    CompletionLog,
    CompletionResult,
    Habit,
    HabitCreate,
    HabitUpdate,
    StreakCalculationRequest,
    StreakResult,
)
from app.services.habit_streaks import calculate_streaks

router = APIRouter(prefix="/api/habits", tags=["habits"])

PREDEFINED_HABITS = [
    Habit(
        id="drink-6-liters-of-water",
        name="Drink 6 Liters of Water",
        description="Drink 6 liters of water per day.",
        weekdays=list(range(7)),
        template_key="drink-6-liters-of-water",
        predefined=True,
    )
]


@router.get("/predefined", response_model=list[Habit])
def list_predefined_habits() -> list[Habit]:
    return PREDEFINED_HABITS


@router.post("", response_model=Habit, status_code=status.HTTP_201_CREATED)
def create_habit(payload: HabitCreate) -> Habit:
    return Habit(**payload.dict())


@router.put("/{habit_id}", response_model=Habit)
def update_habit(habit_id: str, payload: HabitUpdate) -> Habit:
    values = payload.dict(exclude_unset=True)
    if not values:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="at least one field is required",
        )
    if "name" not in values:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="name is required when updating a stateless habit",
        )
    return Habit(id=habit_id, **values)


@router.delete("/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_habit(habit_id: str) -> Response:
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{habit_id}/completion", response_model=CompletionResult)
def log_today_completion(
    habit_id: str, payload: CompletionLog
) -> CompletionResult:
    return CompletionResult(
        habit_id=habit_id,
        completion_date=payload.completion_date,
        completed=payload.completed,
    )


@router.post("/{habit_id}/streak", response_model=StreakResult)
def calculate_habit_streak(
    habit_id: str, payload: StreakCalculationRequest
) -> StreakResult:
    return StreakResult(
        **calculate_streaks(
            completed_dates=payload.completed_dates,
            weekdays=payload.weekdays,
            through=payload.through,
        )
    )