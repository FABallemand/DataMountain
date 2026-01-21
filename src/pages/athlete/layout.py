"""
This module contains the layout of the Athlete page.
"""

import dash
import dash_mantine_components as dmc

from .callbacks import register_callbacks

dash.register_page(__name__, name="Athlete", path="/athlete", order=5)

register_callbacks()

layout = dmc.Container(
    dmc.Stack(
        [
            dmc.Card(
                id={"page": "athlete", "component": "athlete-card"},
            ),
            dmc.Card(
                id={"page": "athlete", "component": "stats-card"},
            ),
            dmc.Card(
                id={"page": "athlete", "component": "gear-card"},
            ),
        ]
    ),
    fluid=True,
)
