"""
This module contains the callbacks of the Home page.
"""

import plotly.express as px
import polars as pl
from dash import Input, Output, State, callback
from dash.exceptions import PreventUpdate


def register_callbacks():
    """
    Register callbacks of the Home page.
    """

    @callback(
        Output({"page": "home", "component": "dist-graph"}, "figure"),
        [
            Input("url", "pathname"),
            Input({"page": "home", "component": "sport-type-select"}, "value"),
        ],
        State("activities-store", "data"),
    )
    def update_dist_graph(_, sport_types, data):
        """
        Update the time graph.
        """
        if sport_types is None or sport_types == []:
            raise PreventUpdate
        if data is None or data == {}:
            raise PreventUpdate
        df = pl.DataFrame(data).filter(pl.col("type").is_in(sport_types))
        return px.line(df, x="start_date_local", y="distance", color="sport_type")

    @callback(
        Output({"page": "home", "component": "time-graph"}, "figure"),
        [
            Input("url", "pathname"),
            Input({"page": "home", "component": "sport-type-select"}, "value"),
        ],
        State("activities-store", "data"),
    )
    def update_time_graph(_, sport_types, data):
        """
        Update the time graph.
        """
        if data is None or data == {}:
            raise PreventUpdate
        df = pl.DataFrame(data).filter(pl.col("type").is_in(sport_types))
        return px.line(df, x="start_date_local", y="elapsed_time", color="sport_type")

    @callback(
        Output({"page": "home", "component": "ele-graph"}, "figure"),
        [
            Input("url", "pathname"),
            Input({"page": "home", "component": "sport-type-select"}, "value"),
        ],
        State("activities-store", "data"),
    )
    def update_ele_graph(_, sport_types, data):
        """
        Update the time graph.
        """
        if data is None or data == {}:
            raise PreventUpdate
        df = pl.DataFrame(data).filter(pl.col("type").is_in(sport_types))
        return px.line(
            df, x="start_date_local", y="total_elevation_gain", color="sport_type"
        )
