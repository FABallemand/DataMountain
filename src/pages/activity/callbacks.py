"""
This module contains the callbacks of the Activities page.
"""

import polars as pl
from dash import Input, Output, State, callback
from dash.exceptions import PreventUpdate


def register_callbacks():
    """
    Register callbacks of the Activities page.
    """

    @callback(
        Output(
            {
                "page": "activity",
                "component": "title",
            },
            "children",
        ),
        Input("url", "pathname"),
        State("activities-store", "data"),
    )
    def update_activity_title(pathname, data):
        """
        Update the Activity page title.
        """
        if pathname is None or "/activity" not in pathname:
            raise PreventUpdate
        if data is None or data == {}:
            raise PreventUpdate

        activity_data = pl.DataFrame(data).filter(
            pl.col("id") == int(pathname.split("/")[-1])
        )

        if activity_data.is_empty():
            return f"Activity with ID {pathname.split('/')[-1]} does not exist..."
        activity_data = activity_data.row(0)
        return f"{activity_data[26]}"
