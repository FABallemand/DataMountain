"""
This module contains the callbacks of the Overview tab of the Activity page.
"""

import polars as pl
from dash import Input, Output, State, callback
from dash.exceptions import PreventUpdate

from constants.colors import SPORT_TYPE_COLORS
from utils.maps import create_map


def register_callbacks():
    """
    Register callbacks of the Overview tab of the Activity page.
    """

    @callback(
        Output(
            {
                "page": "activity",
                "tab": "overview",
                "component": "graph",
            },
            "figure",
        ),
        [
            Input("url", "pathname"),
            Input({"page": "activity", "component": "map-layer-select"}, "value"),
        ],
        State("activities-store", "data"),
    )
    def update_map(pathname, map_layer, data):
        """
        Update the map.
        """
        if pathname is None or "/activity" not in pathname:
            raise PreventUpdate
        if data is None or data == {}:
            raise PreventUpdate

        activity_data = pl.DataFrame(data).filter(
            pl.col("id") == int(pathname.split("/")[-1])
        )

        if activity_data.is_empty():
            raise PreventUpdate

        activity_data = activity_data.row(0)
        return create_map(
            polyline_str=activity_data[22]["summary_polyline"],
            color=SPORT_TYPE_COLORS[activity_data[29]],
            map_layer=map_layer,
        )
