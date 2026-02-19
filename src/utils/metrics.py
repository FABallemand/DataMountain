"""
This module contains the utilities for metrics.
"""


def speed_to_pace(speed: float) -> float:
    """
    Convert speed (in m/s) to pace (in min/km).

    Args:
        speed (float): Speed in m/s.

    Returns:
        float: Pace in min/km.
    """
    if speed == 0:
        return 0
    return 60 / (speed * 3.6)


def pace_to_str(pace: float) -> str:
    """
    Convert pace (in min/km) to a string format (mm:ss).

    Args:
        pace (float): Pace in min/km.

    Returns:
        str: Pace in string format (mm:ss).
    """
    if pace == 0:
        return "0:00"
    minutes = int(pace)
    seconds = int((pace - minutes) * 60)
    return f"{minutes}:{seconds:02d}"
