"""
This module contains the layout of the Home page.
"""

import dash
import dash_mantine_components as dmc
from dash import dcc

from .callbacks import register_callbacks

dash.register_page(__name__, name="Home", path="/", order=1)

register_callbacks()

layout = dmc.Container(
    [
        dmc.Stack(
            [
                dmc.Card(
                    dcc.Graph(id={"page": "home", "component": "dist-graph"}), h="30%"
                ),
                dmc.Card(
                    dcc.Graph(id={"page": "home", "component": "time-graph"}), h="30%"
                ),
                dmc.Card(
                    dcc.Graph(id={"page": "home", "component": "ele-graph"}), h="30%"
                ),
            ],
        ),
    ],
    fluid=True,
)
