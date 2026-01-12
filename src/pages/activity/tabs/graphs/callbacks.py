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

    def safe_div(num, den):
        try:
            return num / den
        except ZeroDivisionError:
            return 0.0

    def create_speed_graph(activity_streams, dist, speed):
        fig = go.Figure()

        # Create hovertemplate and y-stream
        hovertemplate = "Distance: %{x} m<br>" if dist else "Time: %{x}<br>"
        if speed:
            y = [v * 3.6 for v in activity_streams["velocity_smooth"].data]
            hovertemplate += "<br>Speed: %{y:.2f} km/h"
        else:
            y = [
                safe_div(60, v * 3.6) for v in activity_streams["velocity_smooth"].data
            ]
            hovertemplate += "<br>Pace: %{y:.2f} min/km"

        fig.add_trace(
            go.Scatter(
                x=activity_streams["distance"].data
                if dist
                else activity_streams["time"].data,
                y=y,
                hovertemplate=hovertemplate,
                line={"color": "#0000FF"},
            )
        )
        return fig

    def create_ele_graph(activity_streams, dist):
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=activity_streams["distance"].data
                if dist
                else activity_streams["time"].data,
                y=activity_streams["altitude"].data,
                hovertemplate="Distance: %{x} m<br>Elevation: %{y:.2f} m"  # TODO convert to km
                if dist
                else "Time: %{x}<br>Elevation: %{y:.2f} m",
                line={"color": "#00FF00"},
            )
        )
        return fig

    def create_heartrate_graph(activity_streams, dist):
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=activity_streams["distance"].data
                if dist
                else activity_streams["time"].data,
                y=activity_streams["heartrate"].data,
                hovertemplate="Distance: %{x} m<br>Heartrate: %{y:.2f} bpm"
                if dist
                else "Time: %{x}<br>Heartrate: %{y:.2f} bpm",
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
        [
            Input("url", "pathname"),
            Input(
                {
                    "page": "activity",
                    "tab": "graphs",
                    "component": "time-dist-switch",
                },
                "checked",
            ),
            Input(
                {
                    "page": "activity",
                    "tab": "graphs",
                    "component": "pace-speed-switch",
                },
                "checked",
            ),
        ],
        State("activities-store", "data"),
    )
    def update_graphs(pathname, dist, speed, data):
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
            create_speed_graph(activity_streams, dist, speed),
            create_ele_graph(activity_streams, dist),
            create_heartrate_graph(activity_streams, dist),
        )
