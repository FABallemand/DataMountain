"""
This module contains the callbacks of the Home page.
"""

import datetime

import plotly.express as px
import plotly.graph_objects as go
import polars as pl
from dash import Input, Output, callback
from dash.exceptions import PreventUpdate

from constants.colors import SPORT_TYPE_COLORS
from utils.dataframes import create_weekly_df

SPORT_TYPE_ORDER = [
    # Running
    "Run",
    "TrailRun",
    # Cycling
    "Ride",
    "GravelBikeRide",
    "MoutainBikeRide",
    # Walk
    "Walk",
    "Hike",
    "Snowshoe",
    # Other
    "Swim",
]


def register_callbacks():
    """
    Register callbacks of the Home page.
    """

    ## Graphs #########################################################

    def create_plot(df, y):
        hovertemplates = {
            "distance": "Year-Week: %{x}<br>Distance: %{y:.1f} km",
            "elapsed_time": "Year-Week: %{x}<br>Elapsed time: %{y:.1f} min",
            "total_elevation_gain": "Year-Week: %{x}<br>Elevation gain: %{y:.1f} m",
        }
        sport_types = df.get_column("sport_type").unique().sort().to_list()
        # Create figure
        fig = go.Figure()
        for sport_type in sport_types:
            df_sport = df.filter(pl.col("sport_type") == sport_type)
            fig.add_trace(
                go.Scatter(
                    x=df_sport["year_week"].to_list(),
                    y=df_sport[y].to_list(),
                    hovertemplate=hovertemplates[y],
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

    ## Sport Type Bargraph ############################################

    def create_bar(df, y, y_title, color="sport_type"):
        year_weeks = df.get_column("year_week").unique().to_list()
        fig = px.bar(
            df,
            x="year_week",
            y=y,
            color=color,
            color_discrete_map=SPORT_TYPE_COLORS,
            barmode="group",
            category_orders={color: SPORT_TYPE_ORDER},
            text_auto=".2f",
        ).update_layout(
            xaxis={
                "title": None,
                "type": "category",
                "categoryorder": "array",
                "categoryarray": year_weeks,
            },
            yaxis={"title": y_title},
            barcornerradius=15,
        )
        for i in range(len(year_weeks) - 1):
            fig.add_vline(
                x=i + 0.5, line_width=1, line_dash="dot", line_color="gray", opacity=0.4
            )
        return fig

    ## Type Bargraph ##################################################

    def create_bar_type(df, y, y_title):
        year_weeks = df.get_column("year_week").unique().to_list()
        fig = px.histogram(
            df,
            x="year_week",
            y=y,
            color="type",
            color_discrete_map=SPORT_TYPE_COLORS,
            barmode="group",
            category_orders={"type": SPORT_TYPE_ORDER},
            text_auto=".2f",
        ).update_layout(
            xaxis={
                "title": None,
                "type": "category",
                "categoryorder": "array",
                "categoryarray": year_weeks,
            },
            yaxis={"title": y_title},
            barcornerradius=15,
        )
        for i in range(len(year_weeks) - 1):
            fig.add_vline(
                x=i + 0.5, line_width=1, line_dash="dot", line_color="gray", opacity=0.4
            )
        return fig

    ## Callback #######################################################

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
            Input({"page": "home", "component": "graph-type-control"}, "value"),
            Input("activities-store", "data"),
        ],
    )
    def update_graphs(_, sport_types, start_date, stop_date, graph_type, data):
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

        if graph_type == "plot":
            return (
                create_plot(weekly_df, "distance"),
                create_plot(weekly_df, "elapsed_time"),
                create_plot(weekly_df, "total_elevation_gain"),
            )
        if graph_type == "bar_type":
            return (
                create_bar_type(weekly_df, "distance", "Distance"),
                create_bar_type(weekly_df, "elapsed_time", "Elapsed Time"),
                create_bar_type(weekly_df, "total_elevation_gain", "Elevation Gain"),
            )
        if graph_type == "bar_type_sport_type":
            return (
                create_bar(weekly_df, "distance", "Distance", "type"),
                create_bar(weekly_df, "elapsed_time", "Elapsed Time", "type"),
                create_bar(weekly_df, "total_elevation_gain", "Elevation Gain", "type"),
            )
        if graph_type == "bar_sport_type":
            return (
                create_bar(weekly_df, "distance", "Distance"),
                create_bar(weekly_df, "elapsed_time", "Elapsed Time"),
                create_bar(weekly_df, "total_elevation_gain", "Elevation Gain"),
            )
        return None, None, None
