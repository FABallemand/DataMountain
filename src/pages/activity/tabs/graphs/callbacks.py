"""
This module contains the callbacks of the Graphs tab of the Activity page.
"""

import plotly.graph_objects as go
from dash import Input, Output, State, callback
from dash.exceptions import PreventUpdate

from strava.client import CLIENT


def register_callbacks():
    """
    Register callbacks of the Graphs tab of the Activity page.
    """

    def create_speed_graph(activity_streams):
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=activity_streams["distance"].data,
                y=activity_streams["velocity_smooth"].data,
                hovertemplate="Distance: %{x}<br>Speed: %{y:.2f} km/h",
                line={"color": "#0000FF"},
            )
        )
        return fig

    def create_ele_graph(activity_streams):
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=activity_streams["distance"].data,
                y=activity_streams["altitude"].data,
                hovertemplate="Distance: %{x}<br>Elevation: %{y:.2f} km/h",
                line={"color": "#00FF00"},
            )
        )
        return fig

    def create_heartrate_graph(activity_streams):
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=activity_streams["distance"].data,
                y=activity_streams["heartrate"].data,
                hovertemplate="Distance: %{x}<br>Heartrate: %{y:.2f} km/h",
                line={"color": "#FF0000"},
            )
        )
        return fig

    @callback(
        [
            Output(
                {"page": "activity", "tab": "graphs", "component": "speed-graph"},
                "figure",
            ),
            Output(
                {"page": "activity", "tab": "graphs", "component": "ele-graph"},
                "figure",
            ),
            Output(
                {"page": "activity", "tab": "graphs", "component": "heartrate-graph"},
                "figure",
            ),
        ],
        Input("url", "pathname"),
        State("activities-store", "data"),
    )
    def update_graphs(pathname, data):
        """
        Update the graphs.
        """
        if pathname is None or "/activity" not in pathname:
            raise PreventUpdate
        if data is None or data == {}:
            raise PreventUpdate

        # activity_data = pl.DataFrame(data).filter(
        #     pl.col("id") == int(pathname.split("/")[-1])
        # )

        # if activity_data.is_empty():
        #     raise PreventUpdate

        activity_id = int(pathname.split("/")[-1])

        activity_streams = CLIENT.get_activity_streams(
            activity_id,
            ["time", "distance", "velocity_smooth", "altitude", "heartrate"],
        )

        return (
            create_speed_graph(activity_streams),
            create_ele_graph(activity_streams),
            create_heartrate_graph(activity_streams),
        )
