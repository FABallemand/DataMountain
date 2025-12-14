"""
This module contains the callbacks of the Home page.
"""

import plotly.graph_objects as go
import polars as pl
from dash import Input, Output, callback
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
            Input("activities-store", "data"),
        ],
    )
    def update_dist_graph(_, sport_types, data):
        """
        Update the time graph.
        """
        if sport_types is None or sport_types == []:
            raise PreventUpdate
        if data is None or data == {}:
            raise PreventUpdate

        # Create data frame
        df = (
            pl.DataFrame(data)
            .select(["sport_type", "distance", "start_date_local"])
            .filter(pl.col("sport_type").is_in(sport_types))
            .with_columns(
                pl.col("start_date_local").str.to_datetime("%Y-%m-%dT%H:%M:%S+00:00")
            )
            .sort("start_date_local")
            .with_columns(pl.col("start_date_local").dt.week().alias("week"))
            .drop("start_date_local")
            .group_by(["week", "sport_type"])
            .agg(pl.col("distance").sum())
            .with_columns(pl.col("distance") / 1000)  # Convert to km
            .sort("week")
        )

        # Create figure
        fig = go.Figure()
        for sport_type in sport_types:
            df_sport = df.filter(pl.col("sport_type") == sport_type)
            fig.add_trace(
                go.Scatter(
                    x=df_sport["week"].to_list(),
                    y=df_sport["distance"].to_list(),
                    hovertemplate="Week: %{x}<br>Distance: %{y:.1f} km",
                    mode="lines+markers",
                    name=sport_type,
                    stackgroup="one",
                )
            )
        fig.update_layout(
            xaxis={
                "tickmode": "linear",
                "tick0": df.get_column("week").min(),
                "dtick": 1,
            }
        )
        return fig

    @callback(
        Output({"page": "home", "component": "time-graph"}, "figure"),
        [
            Input("url", "pathname"),
            Input({"page": "home", "component": "sport-type-select"}, "value"),
            Input("activities-store", "data"),
        ],
    )
    def update_time_graph(_, sport_types, data):
        """
        Update the time graph.
        """
        if sport_types is None or sport_types == []:
            raise PreventUpdate
        if data is None or data == {}:
            raise PreventUpdate

        # Create data frame
        df = (
            pl.DataFrame(data)
            .select(["sport_type", "elapsed_time", "start_date_local"])
            .filter(pl.col("sport_type").is_in(sport_types))
            .with_columns(
                pl.col("start_date_local").str.to_datetime("%Y-%m-%dT%H:%M:%S+00:00")
            )
            .sort("start_date_local")
            .with_columns(pl.col("start_date_local").dt.week().alias("week"))
            .drop("start_date_local")
            .group_by(["week", "sport_type"])
            .agg(pl.col("elapsed_time").sum())
            .with_columns(pl.col("elapsed_time") / 60)  # Convert to minutes
            .sort("week")
        )

        # Create figure
        fig = go.Figure()
        for sport_type in sport_types:
            df_sport = df.filter(pl.col("sport_type") == sport_type)
            fig.add_trace(
                go.Scatter(
                    x=df_sport["week"].to_list(),
                    y=df_sport["elapsed_time"].to_list(),
                    hovertemplate="Week: %{x}<br>Elapsed time: %{y:.1f} min",
                    mode="lines+markers",
                    name=sport_type,
                    stackgroup="one",
                )
            )
        fig.update_layout(
            xaxis={
                "tickmode": "linear",
                "tick0": df.get_column("week").min(),
                "dtick": 1,
            }
        )
        return fig

    @callback(
        Output({"page": "home", "component": "ele-graph"}, "figure"),
        [
            Input("url", "pathname"),
            Input({"page": "home", "component": "sport-type-select"}, "value"),
            Input("activities-store", "data"),
        ],
    )
    def update_ele_graph(_, sport_types, data):
        """
        Update the time graph.
        """
        if data is None or data == {}:
            raise PreventUpdate

        # Create data frame
        df = (
            pl.DataFrame(data)
            .select(["sport_type", "total_elevation_gain", "start_date_local"])
            .filter(pl.col("sport_type").is_in(sport_types))
            .with_columns(
                pl.col("start_date_local").str.to_datetime("%Y-%m-%dT%H:%M:%S+00:00")
            )
            .sort("start_date_local")
            .with_columns(pl.col("start_date_local").dt.week().alias("week"))
            .drop("start_date_local")
            .group_by(["week", "sport_type"])
            .agg(pl.col("total_elevation_gain").sum())
            .sort("week")
        )

        # Create figure
        fig = go.Figure()
        for sport_type in sport_types:
            df_sport = df.filter(pl.col("sport_type") == sport_type)
            fig.add_trace(
                go.Scatter(
                    x=df_sport["week"].to_list(),
                    y=df_sport["total_elevation_gain"].to_list(),
                    hovertemplate="Week: %{x}<br>Elevation gain: %{y:.1f} m",
                    mode="lines+markers",
                    name=sport_type,
                    stackgroup="one",
                )
            )
        fig.update_layout(
            xaxis={
                "tickmode": "linear",
                "tick0": df.get_column("week").min(),
                "dtick": 1,
            }
        )
        return fig
