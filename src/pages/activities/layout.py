"""
This module contains the layout of the Activities page.
"""

import dash
import dash_mantine_components as dmc

dash.register_page(__name__, name="Activities", path="/activities")

layout = dmc.Box(
    [
        dmc.Title("This is h1 title", order=1),
        dmc.Box("This is our Activities page content."),
    ]
)
