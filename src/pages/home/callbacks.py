"""
This module contains the callbacks of the Home page.
"""

import datetime

import plotly.graph_objects as go
import polars as pl
from dash import Input, Output, callback
from dash.exceptions import PreventUpdate

from constants.colors import SPORT_TYPE_COLORS
from utils.dataframes import create_weekly_df


def register_callbacks():
    """
    Register callbacks of the Home page.
    """

    def create_dist_graph(df):
        sport_types = df.get_column("sport_type").unique().sort().to_list()
        # Create figure
        fig = go.Figure()
        for sport_type in sport_types:
            df_sport = df.filter(pl.col("sport_type") == sport_type)
            fig.add_trace(
                go.Scatter(
                    x=df_sport["year_week"].to_list(),
                    y=df_sport["distance"].to_list(),
                    hovertemplate="Year-Week: %{x}<br>Distance: %{y:.1f} km",
                    mode="lines+markers",
                    name=sport_type,
                    stackgroup="one",
                    line={"color": SPORT_TYPE_COLORS[sport_type]},
                )
            )
        fig.update_layout(
            xaxis={
                "type": "category",
                "categoryorder": "array",
                "categoryarray": df.get_column("year_week").to_list(),
            }
        )
        return fig

    def create_time_graph(df):
        sport_types = df.get_column("sport_type").unique().sort().to_list()
        # Create figure
        fig = go.Figure()
        for sport_type in sport_types:
            df_sport = df.filter(pl.col("sport_type") == sport_type)
            fig.add_trace(
                go.Scatter(
                    x=df_sport["year_week"].to_list(),
                    y=df_sport["elapsed_time"].to_list(),
                    hovertemplate="Year-Week: %{x}<br>Elapsed time: %{y:.1f} min",
                    mode="lines+markers",
                    name=sport_type,
                    stackgroup="one",
                    line={"color": SPORT_TYPE_COLORS[sport_type]},
                )
            )
        fig.update_layout(
            xaxis={
                "type": "category",
                "categoryorder": "array",
                "categoryarray": df.get_column("year_week").to_list(),
            }
        )
        return fig

    def create_ele_graph(df):
        sport_types = df.get_column("sport_type").unique().sort().to_list()
        # Create figure
        fig = go.Figure()
        for sport_type in sport_types:
            df_sport = df.filter(pl.col("sport_type") == sport_type)
            fig.add_trace(
                go.Scatter(
                    x=df_sport["year_week"].to_list(),
                    y=df_sport["total_elevation_gain"].to_list(),
                    hovertemplate="Year-Week: %{x}<br>Elevation gain: %{y:.1f} m",
                    mode="lines+markers",
                    name=sport_type,
                    stackgroup="one",
                    line={"color": SPORT_TYPE_COLORS[sport_type]},
                )
            )
        fig.update_layout(
            xaxis={
                "type": "category",
                "categoryorder": "array",
                "categoryarray": df.get_column("year_week").to_list(),
            }
        )
        return fig

    @callback(
        [
            Output({"page": "home", "component": "dist-graph"}, "figure"),
            Output({"page": "home", "component": "time-graph"}, "figure"),
            Output({"page": "home", "component": "ele-graph"}, "figure"),
        ],
        [
            Input("url", "pathname"),
            Input({"page": "home", "component": "sport-type-select"}, "value"),
            Input({"page": "home", "component": "start-date-picker"}, "value"),
            Input({"page": "home", "component": "stop-date-picker"}, "value"),
            Input("activities-store", "data"),
        ],
    )
    def update_graphs(_, sport_types, start_date, stop_date, data):
        """
        Update the graphs.
        """
        if sport_types is None or sport_types == []:
            raise PreventUpdate
        if data is None or data == {}:
            raise PreventUpdate

        # Convert start and stop dates
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        stop_date = datetime.datetime.strptime(stop_date, "%Y-%m-%d").date()

        # Create dataframe from data
        weekly_df = create_weekly_df(
            pl.DataFrame(data), sport_types, start_date, stop_date
        ).with_columns(
            pl.concat_str([pl.col("iso_year"), pl.lit("-"), pl.col("iso_week")]).alias(
                "year_week"
            )
        )

        return (
            create_dist_graph(weekly_df),
            create_time_graph(weekly_df),
            create_ele_graph(weekly_df),
        )
