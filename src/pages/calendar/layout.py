"""
This module contains the layout of the Calendar page.
"""

import dash
import dash_mantine_components as dmc

from .callbacks import register_callbacks

dash.register_page(__name__, name="Calendar", path="/calendar", order=2)

register_callbacks()

layout = dmc.Container(
    dmc.Card(
        dmc.TableScrollContainer(
            dmc.Table(
                id={"page": "calendar", "component": "calendar"},
                striped=False,
                highlightOnHover=True,
                withTableBorder=True,
                withColumnBorders=True,
                stickyHeader=True,
            ),
            type="scrollarea",
            minWidth="100%",
            style={"height": "80vh"},
        ),
    ),
    fluid=True,
)
