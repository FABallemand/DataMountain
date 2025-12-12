"""
This module contains the callbacks of the Activities page.
"""

from dash import Input, Output, State, callback
from dash.exceptions import PreventUpdate


def register_callbacks():
    """
    Register callbacks of the Activities page.
    """

    @callback(
        Output({"page": "activities", "component": "activities-table"}, "rowData"),
        Input("url", "pathname"),
        State("activities-store", "data"),
    )
    def update_activities_table(pathname, data):
        """
        Update the activities table.
        """
        if pathname is None or "/activities" not in pathname:
            raise PreventUpdate

        if data is None or data == {}:
            raise PreventUpdate

        return data
