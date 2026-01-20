"""
This module contains the utilities for dates.
"""

import datetime


def iso_weeks_in_year(year: int) -> int:
    """
    Return number of ISO calendar weeks in a given year.
    """
    return datetime.date(year, 12, 28).isocalendar().week


def monday_of_week(d: datetime.date) -> datetime.date:
    """
    Return the Monday of the week containing the given date.
    """
    return d - datetime.timedelta(days=d.isoweekday() - 1)
