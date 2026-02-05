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

    def create_dist_plot(df):
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

    def create_time_plot(df):
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

    def create_ele_plot(df):
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

    ## Sport Type Bargraph ############################################

    def create_dist_bar(df, color="sport_type"):
        return px.bar(
            df,
            x="year_week",
            y="distance",
            color=color,
            color_discrete_map=SPORT_TYPE_COLORS,
            barmode="group",
            category_orders={color: SPORT_TYPE_ORDER},
            text_auto=".2f",
        ).update_layout(
            xaxis={"title": None, "type": "category"},
            yaxis={"title": "Distance"},
            barcornerradius=15,
        )

    def create_time_bar(df, color="sport_type"):
        return px.bar(
            df,
            x="year_week",
            y="elapsed_time",
            color=color,
            color_discrete_map=SPORT_TYPE_COLORS,
            barmode="group",
            category_orders={color: SPORT_TYPE_ORDER},
            text_auto=".2f",
        ).update_layout(
            xaxis={"title": None, "type": "category"},
            yaxis={"title": "Elapsed Time"},
            barcornerradius=15,
        )

    def create_ele_bar(df, color="sport_type"):
        return px.bar(
            df,
            x="year_week",
            y="total_elevation_gain",
            color=color,
            color_discrete_map=SPORT_TYPE_COLORS,
            barmode="group",
            category_orders={color: SPORT_TYPE_ORDER},
            text_auto=".2f",
        ).update_layout(
            xaxis={"title": None, "type": "category"},
            yaxis={"title": "Elevation Gain"},
            barcornerradius=15,
        )

    ## Type Bargraph ##################################################

    def create_dist_bar_type(df):
        return px.histogram(
            df,
            x="year_week",
            y="distance",
            color="type",
            color_discrete_map=SPORT_TYPE_COLORS,
            barmode="group",
            category_orders={"type": SPORT_TYPE_ORDER},
            text_auto=".2f",
        ).update_layout(
            xaxis={"title": None, "type": "category"},
            yaxis={"title": "Distance"},
            barcornerradius=15,
        )

    def create_time_bar_type(df):
        return px.histogram(
            df,
            x="year_week",
            y="elapsed_time",
            color="type",
            color_discrete_map=SPORT_TYPE_COLORS,
            barmode="group",
            category_orders={"type": SPORT_TYPE_ORDER},
            text_auto=".2f",
        ).update_layout(
            xaxis={"title": None, "type": "category"},
            yaxis={"title": "Elapsed Time"},
            barcornerradius=15,
        )

    def create_ele_bar_type(df):
        return px.histogram(
            df,
            x="year_week",
            y="total_elevation_gain",
            color="type",
            color_discrete_map=SPORT_TYPE_COLORS,
            barmode="group",
            category_orders={"type": SPORT_TYPE_ORDER},
            text_auto=".2f",
        ).update_layout(
            xaxis={"title": None, "type": "category"},
            yaxis={"title": "Elevation Gain"},
            barcornerradius=15,
        )

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
                create_dist_plot(weekly_df),
                create_time_plot(weekly_df),
                create_ele_plot(weekly_df),
            )
        if graph_type == "bar_type":
            return (
                create_dist_bar_type(weekly_df),
                create_time_bar_type(weekly_df),
                create_ele_bar_type(weekly_df),
            )
        if graph_type == "bar_type_sport_type":
            return (
                create_dist_bar(weekly_df, "type"),
                create_time_bar(weekly_df, "type"),
                create_ele_bar(weekly_df, "type"),
            )
        if graph_type == "bar_sport_type":
            return (
                create_dist_bar(weekly_df),
                create_time_bar(weekly_df),
                create_ele_bar(weekly_df),
            )
        return None, None, None
