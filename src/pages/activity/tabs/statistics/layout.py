# pylint: disable=invalid-name
# Disable invalid name to match dash PascalCase
"""
This module contains the layout of the Statistics tab of the Activity page.
"""

import dash_mantine_components as dmc

from .callbacks import register_callbacks

register_callbacks()


def StatisticsLayout():
    """
    Create the layout of the Statistics tab of the Activity page.
    """
    return dmc.Stack(
        [
            dmc.Title("General", order=2),
            dmc.Table(
                id={
                    "page": "activity",
                    "tab": "statistics",
                    "component": "general-table",
                },
                striped=True,
                highlightOnHover=True,
                withTableBorder=True,
                withColumnBorders=False,
            ),
            dmc.Title("Performance", order=2),
            dmc.Table(
                id={
                    "page": "activity",
                    "tab": "statistics",
                    "component": "perf-table",
                },
                striped=True,
                highlightOnHover=True,
                withTableBorder=True,
                withColumnBorders=False,
            ),
            dmc.Title("Gear", order=2),
            # TODO
            dmc.Title("Location", order=2),
            dmc.Table(
                id={
                    "page": "activity",
                    "tab": "statistics",
                    "component": "location-table",
                },
                striped=True,
                highlightOnHover=True,
                withTableBorder=True,
                withColumnBorders=False,
            ),
            dmc.Title("Time", order=2),
            dmc.Table(
                id={
                    "page": "activity",
                    "tab": "statistics",
                    "component": "time-table",
                },
                striped=True,
                highlightOnHover=True,
                withTableBorder=True,
                withColumnBorders=False,
            ),
            dmc.Title("Strava", order=2),
            dmc.Table(
                id={
                    "page": "activity",
                    "tab": "statistics",
                    "component": "strava-table",
                },
                striped=True,
                highlightOnHover=True,
                withTableBorder=True,
                withColumnBorders=False,
            ),
        ]
    )
