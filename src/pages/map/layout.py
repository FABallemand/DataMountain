"""
This module contains the layout of the Map page.
"""

import dash
import dash_mantine_components as dmc
from dash import dcc

from .callbacks import register_callbacks

dash.register_page(__name__, name="Map", path="/map", order=4)

register_callbacks()

layout = dmc.Container(
    dmc.Card(
        dcc.Graph(id={"page": "map", "component": "map"}, style={"height": "80vh"})
    ),
    fluid=True,
)
