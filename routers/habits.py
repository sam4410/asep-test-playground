import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import Habit, HabitCheckin, User
from schemas import (
    HabitCreate,
    HabitUpdate,
    HabitResponse,
    HeatmapDay,
    CheckinCreate,
    CheckinResponse,
    DashboardStats,
)
from auth_utils import get_current_user

router = APIRouter(tags=["habits"])


def _get_owned_habit(habit_id: str, user: User, db: Session) -> Habit:
    habit = (
        db.query(Habit)
        .filter(Habit.id == habit_id, Habit.user_id == user.id)
        .first()
    )
    if not habit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Habit not found")
    return habit


def _compute_streaks(checkin_dates: set, target_frequency: int, today: datetime.date):
    """Compute current and longest streak in terms of consecutive days checked off.

    Streak logic: a streak continues day-over-day as long as a check-in exists.
    A missed day breaks the current streak (grace is not applied here since
    target_frequency governs weekly completion percentage, not streak length).
    """
    if not checkin_dates:
        return 0, 0

    sorted_dates = sorted(checkin_dates)

    longest_streak = 1
    run = 1
    for i in range(1, len(sorted_dates)):
        if (sorted_dates[i] - sorted_dates[i - 1]).days == 1:
            run += 1
        else:
            run = 1
        longest_streak = max(longest_streak, run)

    # Current streak: count backwards from today (or yesterday if today not
    # yet checked in, so a single missed "today" doesn't erase history mid-day).
    current_streak = 0
    cursor = today
    if today not in checkin_dates:
        cursor = today - datetime.timedelta(days=1)
    while cursor in checkin_dates:
        current_streak += 1
        cursor -= datetime.timedelta(days=1)

    return current_streak, longest_streak


def _build_weekly_heatmap(checkin_dates: set, today: datetime.date) -> List[HeatmapDay]:
    days = []
    for offset in range(6, -1, -1):
        day = today - datetime.timedelta(days=offset)
        days.append(HeatmapDay(date=day, completed=day in checkin_dates))
    return days


def _habit_to_response(habit: Habit) -> HabitResponse:
    today = datetime.date.today()
    checkin_dates = {c.date for c in habit.checkins}
    current_streak, longest_streak = _compute_streaks(checkin_dates, habit.target_frequency, today)
    weekly_heatmap = _build_weekly_heatmap(checkin_dates, today)

    return HabitResponse(
        id=habit.id,
        name=habit.name,
        target_frequency=habit.target_frequency,
        created_at=habit.created_at,
        current_streak=current_streak,
        longest_streak=longest_streak,
        weekly_heatmap=weekly_heatmap,
        completed_today=today in checkin_dates,
    )


@router.get("/habits", response_model=List[HabitResponse])
def list_habits(
    include_archived: bool = False,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(Habit).filter(Habit.user_id == current_user.id)
    if not include_archived:
        query = query.filter(Habit.is_archived.is_(False))
    habits = query.order_by(Habit.created_at.desc()).all()
    return [_habit_to_response(h) for h in habits]


@router.post("/habits", response_model=HabitResponse, status_code=status.HTTP_201_CREATED)
def create_habit(
    payload: HabitCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    habit = Habit(
        user_id=current_user.id,
        name=payload.name,
        target_frequency=payload.target_frequency,
    )
    db.add(habit)
    db.commit()
    db.refresh(habit)
    return _habit_to_response(habit)


@router.get("/habits/{habit_id}", response_model=HabitResponse)
def get_habit(
    habit_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    habit = _get_owned_habit(habit_id, current_user, db)
    return _habit_to_response(habit)


@router.put("/habits/{habit_id}", response_model=HabitResponse)
def update_habit(
    habit_id: str,
    payload: HabitUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    habit = _get_owned_habit(habit_id, current_user, db)

    if payload.name is not None:
        habit.name = payload.name
    if payload.target_frequency is not None:
        habit.target_frequency = payload.target_frequency
    if payload.is_archived is not None:
        habit.is_archived = payload.is_archived

    db.commit()
    db.refresh(habit)
    return _habit_to_response(habit)


@router.delete("/habits/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_habit(
    habit_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    habit = _get_owned_habit(habit_id, current_user, db)
    db.delete(habit)
    db.commit()
    return None


@router.post("/habits/{habit_id}/checkin", response_model=CheckinResponse, status_code=status.HTTP_201_CREATED)
def checkin_habit(
    habit_id: str,
    payload: CheckinCreate = CheckinCreate(),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    habit = _get_owned_habit(habit_id, current_user, db)
    checkin_date = payload.date or datetime.date.today()

    existing = (
        db.query(HabitCheckin)
        .filter(HabitCheckin.habit_id == habit.id, HabitCheckin.date == checkin_date)
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Habit already checked in for this date.",
        )

    checkin = HabitCheckin(habit_id=habit.id, date=checkin_date)
    db.add(checkin)
    db.commit()
    db.refresh(habit)

    today = datetime.date.today()
    checkin_dates = {c.date for c in habit.checkins}
    current_streak, longest_streak = _compute_streaks(checkin_dates, habit.target_frequency, today)

    return CheckinResponse(
        id=checkin.id,
        habit_id=habit.id,
        date=checkin.date,
        current_streak=current_streak,
        longest_streak=longest_streak,
        completed_today=today in checkin_dates,
    )


@router.delete("/habits/{habit_id}/checkin", status_code=status.HTTP_204_NO_CONTENT)
def uncheck_habit(
    habit_id: str,
    checkin_date: Optional[datetime.date] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    habit = _get_owned_habit(habit_id, current_user, db)
    target_date = checkin_date or datetime.date.today()

    checkin = (
        db.query(HabitCheckin)
        .filter(HabitCheckin.habit_id == habit.id, HabitCheckin.date == target_date)
        .first()
    )
    if not checkin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Check-in not found")

    db.delete(checkin)
    db.commit()
    return None


@router.get("/dashboard/stats", response_model=DashboardStats)
def get_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    today = datetime.date.today()

    all_habits = db.query(Habit).filter(Habit.user_id == current_user.id).all()
    active_habits = [h for h in all_habits if not h.is_archived]

    total_habits = len(all_habits)
    active_habit_count = len(active_habits)

    total_checkins_today = 0
    completion_ratios = []

    for habit in active_habits:
        checkin_dates = {c.date for c in habit.checkins}
        if today in checkin_dates:
            total_checkins_today += 1

        window_start = today - datetime.timedelta(days=6)
        window_checkins = sum(1 for d in checkin_dates if window_start <= d <= today)
        target = max(habit.target_frequency, 1) * 7 / 7  # per-day target baseline
        expected = max(habit.target_frequency, 1)
        ratio = min(window_checkins / expected, 1.0) if expected else 0.0
        completion_ratios.append(ratio)

    daily_completion = (
        total_checkins_today / active_habit_count if active_habit_count else 0.0
    )
    overall_completion_percentage = (
        (sum(completion_ratios) / len(completion_ratios)) * 100 if completion_ratios else 0.0
    )

    return DashboardStats(
        active_habit_count=active_habit_count,
        daily_completion=round(daily_completion, 4),
        overall_completion_percentage=round(overall_completion_percentage, 2),
        total_checkins_today=total_checkins_today,
        total_habits=total_habits,
    )