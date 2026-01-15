# pylint: disable=invalid-name
# Disable invalid name to match dash PascalCase
"""
This module contains the layout of the Graphs tab of the Activity page.
"""

import dash_mantine_components as dmc
from dash import dcc, html

from .callbacks import register_callbacks

register_callbacks()


def GraphsLayout():
    """
    Create the layout of the Graphs tab of the Activity page.
    """
    return dmc.Stack(
        [
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
            dmc.Card(
                html.Iframe(
                    id={
                        "page": "activity",
                        "tab": "graphs",
                        "component": "map",
                    },
                    style={"height": "70vh"},
                ),
            ),
        ]
    )
