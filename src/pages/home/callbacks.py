"""
This module contains the callbacks of the Home page.
"""

import datetime

import plotly.graph_objects as go
import polars as pl
from dash import Input, Output, callback
from dash.exceptions import PreventUpdate

from constants.colors import SPORT_TYPE_COLORS


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
    def update_dist_graph(_, sport_types, start_date, stop_date, data):
        """
        Update the time graph.
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
            .select(
                [
                    "sport_type",
                    "start_date_local",
                    "distance",
                    "elapsed_time",
                    "total_elevation_gain",
                ]
            )
            .with_columns(
                pl.col("start_date_local").str.to_datetime("%Y-%m-%dT%H:%M:%S+00:00")
            )
            .filter(
                (pl.col("sport_type").is_in(sport_types))
                & (pl.col("start_date_local").is_between(start_date, stop_date))
            )
        )

        # Aggregate distances by week and sport type
        weekly_df = (
            df.with_columns(
                pl.col("start_date_local").dt.iso_year().alias("iso_year"),
                pl.col("start_date_local").dt.week().alias("week"),
            )
            .with_columns(
                pl.concat_str([pl.col("iso_year"), pl.lit("-"), pl.col("week")]).alias(
                    "year_week"
                )
            )
            .group_by(["year_week", "sport_type"])
            .agg(
                [
                    pl.col("distance").sum() / 1000,  # Convert to km
                    pl.col("elapsed_time").sum() / 60,  # Convert to minutes
                    pl.col("total_elevation_gain").sum(),
                ]
            )
            .sort(["year_week"])
        )

        # Create calendar of weeks
        calendar = (
            pl.date_range(start_date, stop_date, interval="1w", eager=True)
            .to_frame("date")
            .with_columns(
                pl.col("date").dt.iso_year().alias("iso_year"),
                pl.col("date").dt.week().alias("week"),
            )
            .with_columns(
                pl.format("{}-{}", pl.col("iso_year"), pl.col("week")).alias(
                    "year_week"
                )
            )
            .select("year_week")
            .unique()
            .sort("year_week")
        )

        # Retrieve sports types
        sports = pl.DataFrame(
            {"sport_type": df.select("sport_type").unique().to_series().to_list()}
        )

        # Create full index of year_week and sport_type
        full_index = calendar.join(sports, how="cross")

        # Merge with weekly_df to fill missing weeks/sport types with 0 distance
        final_df = (
            full_index.join(weekly_df, on=["year_week", "sport_type"], how="left")
            .with_columns(pl.col("distance").fill_null(0))
            .sort(["year_week", "sport_type"])
        )

        return (
            create_dist_graph(final_df),
            create_time_graph(final_df),
            create_ele_graph(final_df),
        )
