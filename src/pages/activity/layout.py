"""
This module contains the layout of the Activity page.
"""

import dash
import dash_mantine_components as dmc

from .callbacks import register_callbacks

dash.register_page(
    __name__, name="Activity", path_template="/activity/<activity_id>", order=None
)

register_callbacks()


def layout(activity_id):
    """
    Define the layout of the Activity page.
    """
    return dmc.Container(
        id={
            "page": "activity",
            "component": "main-container",
        },
        fluid=True,
    )
