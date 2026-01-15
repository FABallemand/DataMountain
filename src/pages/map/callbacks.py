"""
This module contains the callbacks of the Map page.
"""

import datetime

import numpy as np
import plotly.graph_objects as go
import polars as pl
from dash import Input, Output, callback
from dash.exceptions import PreventUpdate

from constants.colors import SPORT_TYPE_COLORS
from utils.maps import create_scattermap


def register_callbacks():
    """
    Register callbacks of the Map page.
    """

    @callback(
        Output({"page": "map", "component": "map"}, "figure"),
        [
            Input("url", "pathname"),
            Input({"page": "map", "component": "sport-type-select"}, "value"),
            Input({"page": "map", "component": "start-date-picker"}, "value"),
            Input({"page": "map", "component": "stop-date-picker"}, "value"),
            Input({"page": "map", "component": "map-layer-select"}, "value"),
            Input("activities-store", "data"),
        ],
    )
    def update_graph(_, sport_types, start_date, stop_date, map_layer, data):
        """
        Update the graph.
        """
        if sport_types is None or sport_types == []:
            raise PreventUpdate
        if data is None or data == {}:
            raise PreventUpdate

        # Convert start and stop dates
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        stop_date = datetime.datetime.strptime(stop_date, "%Y-%m-%d")

        # Create dataframe from data
        df = (
            pl.DataFrame(data)
            .with_columns(
                pl.col("start_date_local").str.to_datetime("%Y-%m-%dT%H:%M:%S+00:00")
            )
            .filter(
                (pl.col("sport_type").is_in(sport_types))
                & (pl.col("start_date_local").is_between(start_date, stop_date))
            )
        )

        fig = go.Figure()
        center_lats = []
        center_lons = []
        for row in df.iter_rows():
            scattermap, center_lat, center_lon = create_scattermap(
                row[22]["summary_polyline"],
                name=row[26],
                color=SPORT_TYPE_COLORS.get(row[29], "#FFA800"),
            )
            fig.add_trace(scattermap)
            center_lats.append(center_lat)
            center_lons.append(center_lon)

        fig.update_layout(
            margin={"l": 0, "t": 0, "b": 0, "r": 0},
            map={
                "center": {"lon": np.mean(center_lons), "lat": np.mean(center_lats)},
                "style": map_layer,
                "zoom": 10,
            },
            title={"text": "test"},
        )

        return fig
