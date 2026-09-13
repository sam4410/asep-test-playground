from datetime import date, timedelta

import pytest
from pydantic import ValidationError

from app.schemas.habits import (
    CompletionLog,
    HabitCreate,
    HabitUpdate,
    StreakCalculationRequest,
)
from app.services.habit_streaks import calculate_streak, calculate_streaks


def test_calculate_streaks_counts_consecutive_scheduled_days():
    through = date(2024, 1, 5)  # Friday
    completed = [
        date(2024, 1, 1),  # Monday
        date(2024, 1, 3),  # Wednesday
        date(2024, 1, 5),  # Friday
    ]

    assert calculate_streaks(completed, [0, 2, 4], through) == {
        "current_streak": 3,
        "longest_streak": 3,
    }


def test_missed_scheduled_day_breaks_current_and_longest_streaks():
    through = date(2024, 1, 5)
    completed = [
        date(2024, 1, 1),  # Monday
        date(2024, 1, 5),  # Friday; Wednesday was missed
    ]

    assert calculate_streaks(completed, [0, 2, 4], through) == {
        "current_streak": 1,
        "longest_streak": 1,
    }


def test_unscheduled_days_do_not_break_a_streak():
    through = date(2024, 1, 5)
    completed = [date(2024, 1, 1), date(2024, 1, 5)]

    assert calculate_streaks(completed, [0, 4], through) == {
        "current_streak": 2,
        "longest_streak": 2,
    }


def test_current_streak_can_differ_from_longest_historical_streak():
    through = date(2024, 1, 10)  # Wednesday
    completed = [
        date(2024, 1, 1),  # Monday
        date(2024, 1, 5),  # Friday
        date(2024, 1, 8),  # Monday
    ]

    assert calculate_streaks(completed, [0, 4], through) == {
        "current_streak": 3,
        "longest_streak": 3,
    }


def test_empty_history_returns_zero_streaks():
    assert calculate_streaks([], [0, 1, 2], date(2024, 1, 10)) == {
        "current_streak": 0,
        "longest_streak": 0,
    }


def test_empty_schedule_returns_zero_streaks():
    assert calculate_streaks([date(2024, 1, 1)], [], date(2024, 1, 1)) == {
        "current_streak": 0,
        "longest_streak": 0,
    }


def test_dates_after_through_are_ignored_at_date_boundary():
    through = date(2024, 1, 5)
    completed = [through, through + timedelta(days=1)]

    assert calculate_streaks(completed, [4], through) == {
        "current_streak": 1,
        "longest_streak": 1,
    }


def test_calculate_streak_alias_matches_calculate_streaks():
    completed = [date(2024, 1, 1), date(2024, 1, 2)]
    through = date(2024, 1, 2)

    assert calculate_streak(completed, [0, 1], through) == calculate_streaks(
        completed, [0, 1], through
    )


@pytest.mark.parametrize(
    "weekdays",
    [
        [],
        [0, 0],
        [-1],
        [7],
        [0, 1, 8],
    ],
)
def test_habit_schemas_reject_invalid_weekday_schedules(weekdays):
    with pytest.raises(ValidationError):
        HabitCreate(name="Meditate", weekdays=weekdays)

    with pytest.raises(ValidationError):
        HabitUpdate(weekdays=weekdays)

    with pytest.raises(ValidationError):
        StreakCalculationRequest(weekdays=weekdays)


def test_habit_schema_sorts_valid_weekdays():
    habit = HabitCreate(name="Meditate", weekdays=[4, 1, 6])

    assert habit.weekdays == [1, 4, 6]


def test_habit_schema_rejects_blank_names():
    with pytest.raises(ValidationError):
        HabitCreate(name="   ")

    with pytest.raises(ValidationError):
        HabitUpdate(name=" ")


def test_completion_log_accepts_only_the_current_local_date():
    today = date.today()

    completion = CompletionLog(
        local_today=today,
        completion_date=today,
        completed=True,
    )

    assert completion.completion_date == today
    assert completion.completed is True


def test_completion_log_rejects_past_completion_dates():
    today = date.today()

    with pytest.raises(ValidationError):
        CompletionLog(
            local_today=today,
            completion_date=today - timedelta(days=1),
        )


def test_completion_log_rejects_future_local_today():
    tomorrow = date.today() + timedelta(days=1)

    with pytest.raises(ValidationError):
        CompletionLog(
            local_today=tomorrow,
            completion_date=tomorrow,
        )


def test_streak_request_rejects_a_future_through_date():
    with pytest.raises(ValidationError):
        StreakCalculationRequest(
            completed_dates=[],
            weekdays=[0],
            through=date.today() + timedelta(days=1),
        )


def test_streak_request_defaults_to_empty_history_and_daily_schedule():
    request = StreakCalculationRequest()

    assert request.completed_dates == []
    assert request.weekdays == [0, 1, 2, 3, 4, 5, 6]
    assert request.through == date.today()