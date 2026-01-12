# pylint: disable=invalid-name
# Disable invalid name to match dash PascalCase
"""
This module contains the layout of the Graphs tab of the Activity page.
"""

import dash_mantine_components as dmc
from dash import dcc

from .callbacks import register_callbacks

register_callbacks()


def GraphsLayout():
    """
    Create the layout of the Graphs tab of the Activity page.
    """
    return dmc.Stack(
        [
            dmc.Card(
                dmc.Group(
                    [
                        dmc.Switch(
                            id={
                                "page": "activity",
                                "tab": "graphs",
                                "component": "time-dist-switch",
                            },
                            offLabel="Time",
                            onLabel="Distance",
                            checked="False",
                            size="lg",
                        ),
                        dmc.Switch(
                            id={
                                "page": "activity",
                                "tab": "graphs",
                                "component": "pace-speed-switch",
                            },
                            offLabel="Pace",
                            onLabel="Speed",
                            checked="False",
                            size="lg",
                        ),
                    ]
                )
            ),
            dmc.Card(
                dcc.Graph(
                    id={
                        "page": "activity",
                        "tab": "graphs",
                        "component": "speed-graph",
                    },
                ),
            ),
            dmc.Card(
                dcc.Graph(
                    id={
                        "page": "activity",
                        "tab": "graphs",
                        "component": "ele-graph",
                    },
                ),
            ),
            dmc.Card(
                dcc.Graph(
                    id={
                        "page": "activity",
                        "tab": "graphs",
                        "component": "heartrate-graph",
                    },
                ),
            ),
        ]
    )
