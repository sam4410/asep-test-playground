from datetime import date, timedelta
from your_project_name.api.db.models import Habit

def calculate_streak(habit: Habit, check_in_date: date):
    # Get the current streak and last check-in date
    current_streak = habit.streak_count
    last_check_in_date = habit.last_check_in_date  # Assuming this field exists

    if last_check_in_date is None:
        # If there's no previous check-in, start a new streak
        habit.streak_count = 1
        habit.last_check_in_date = check_in_date
        return habit.streak_count

    # Calculate the difference in days between the last check-in and the current check-in
    days_difference = (check_in_date - last_check_in_date).days

    if days_difference == 1:
        # Increment streak if checked in on consecutive days
        habit.streak_count += 1
    elif days_difference > 1:
        # Reset streak if checked in after a gap
        habit.streak_count = 1

    # Update the last check-in date
    habit.last_check_in_date = check_in_date
    return habit.streak_count

def check_in_habit(habit: Habit, check_in_date: date):
    return calculate_streak(habit, check_in_date)
