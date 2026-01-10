# pylint: disable=invalid-name
# Disable invalid name to match dash PascalCase
"""
This module contains the layout of the Statistics tab of the Activity page.
"""

import dash_mantine_components as dmc

from .callbacks import register_callbacks

register_callbacks()


def LeftColLayout():
    """
    Create the layout of the left column of Statistics.
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
            dmc.Table(
                id={
                    "page": "activity",
                    "tab": "statistics",
                    "component": "gear-table",
                },
                striped=True,
                highlightOnHover=True,
                withTableBorder=True,
                withColumnBorders=False,
            ),
        ]
    )


def RightColLayout():
    """
    Create the layout of the right column of Statistics.
    """
    return dmc.Stack(
        [
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
        ],
    )


def StatisticsLayout():
    """
    Create the layout of the Statistics tab of the Activity page.
    """
    return dmc.Card(
        dmc.Group(
            [LeftColLayout(), RightColLayout()],
            id={
                "page": "activity",
                "tab": "statistics",
                "component": "stats-grid",
            },
            justify="space-around",
            gap="xs",
            grow=True,
        )
    )
