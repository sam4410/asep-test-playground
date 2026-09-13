from datetime import date, timedelta
from typing import Iterable, Set


def calculate_streaks(
    completed_dates: Iterable[date],
    weekdays: Iterable[int],
    through: date | None = None,
) -> dict[str, int]:
    """Calculate current and longest streaks over scheduled weekdays."""
    end = through or date.today()
    scheduled: Set[int] = set(weekdays)
    completed: Set[date] = {
        completed_date
        for completed_date in completed_dates
        if completed_date <= end
    }

    if not scheduled or not completed:
        return {"current_streak": 0, "longest_streak": 0}

    current = 0
    cursor = end
    while cursor >= date.min:
        if cursor.weekday() in scheduled:
            if cursor not in completed:
                break
            current += 1
        cursor -= timedelta(days=1)

    longest = 0
    run = 0
    cursor = min(completed)
    while cursor <= end:
        if cursor.weekday() in scheduled:
            if cursor in completed:
                run += 1
                longest = max(longest, run)
            else:
                run = 0
        cursor += timedelta(days=1)

    return {"current_streak": current, "longest_streak": longest}


def calculate_streak(
    completed_dates: Iterable[date],
    weekdays: Iterable[int],
    through: date | None = None,
) -> dict[str, int]:
    return calculate_streaks(completed_dates, weekdays, through)
