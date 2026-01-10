# pylint: disable=invalid-name
# Disable invalid name to match dash PascalCase
"""
This module contains the layout of the Overview tab of the Activity page.
"""

import dash_mantine_components as dmc
from dash import dcc

from .callbacks import register_callbacks

register_callbacks()


def OverviewLayout():
    """
    Create the layout of the Overview tab of the Activity page.
    """
    return dmc.Stack(
        [
            dcc.Graph(
                id={
                    "page": "activity",
                    "tab": "overview",
                    "component": "graph",
                },
            ),
            dmc.SimpleGrid(
                id={
                    "page": "activity",
                    "tab": "overview",
                    "component": "stats",
                },
                cols=4,
                spacing="md",
                verticalSpacing="md",
            ),
        ]
    )
