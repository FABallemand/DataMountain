# pylint: disable=invalid-name
# Disable invalid name to match dash PascalCase
"""
This module contains the layout of the Statistics tab of the Activity page.
"""

import dash_mantine_components as dmc

from .callbacks import register_callbacks

register_callbacks()


def FirstRowLayout():
    """
    Create the layout of the first row of the Statistics tab.
    """
    return dmc.Group(
        [
            dmc.Stack(
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
                ]
            ),
            dmc.Stack(
                [
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
                ]
            ),
        ],
        grow=True,
        align="flex-start",
    )


def SecondRowLayout():
    """
    Create the layout of the second row of the Statistics tab.
    """
    return dmc.Group(
        [
            dmc.Stack(
                [
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
                ],
            ),
            dmc.Stack(
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
                ]
            ),
        ],
        grow=True,
        align="flex-start",
    )


def ThirdRowLayout():
    """
    Create the layout of the third row of the Statistics tab.
    """
    return dmc.Group(
        [
            dmc.Stack(
                [
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
            ),
            dmc.Stack(
                [
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
            ),
        ],
        grow=True,
        align="flex-start",
    )


def StatisticsLayout():
    """
    Create the layout of the Statistics tab of the Activity page.
    """
    return dmc.Card(
        dmc.Stack(
            [FirstRowLayout(), SecondRowLayout(), ThirdRowLayout()],
        )
    )
