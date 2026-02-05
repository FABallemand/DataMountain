"""
This module contains the utilities for dates.
"""

import datetime


def iso_weeks_in_year(year: int) -> int:
    """
    Return number of ISO calendar weeks in a given year.
    """
    return datetime.date(year, 12, 28).isocalendar().week


def monday_of_week(date: datetime.date) -> datetime.date:
    """
    Return the Monday of the week containing the given date.
    """
    return date - datetime.timedelta(days=date.isoweekday() - 1)


def duration_to_string(seconds: float | int) -> str:
    """
    Convert a duration in seconds to a human readable format.
    """
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"
