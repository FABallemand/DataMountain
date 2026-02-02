"""
This module contains the callbacks of the Graphs tab of the Activity page.
"""

import folium
import numpy as np
import plotly.graph_objects as go
from dash import Input, Output, State, callback
from dash.exceptions import PreventUpdate

from constants.colors import COLORMAPS
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

    def create_speed_graph(activity_streams, time, pace):
        fig = go.Figure()

        # Create hovertemplate and y-stream
        hovertemplate = "Time: %{x}<br>" if time else "Distance: %{x} m<br>"
        if pace:
            y = [
                safe_div(60, v * 3.6) for v in activity_streams["velocity_smooth"].data
            ]
            hovertemplate += "<br>Pace: %{y:.2f} min/km"
        else:
            y = [v * 3.6 for v in activity_streams["velocity_smooth"].data]
            hovertemplate += "<br>Speed: %{y:.2f} km/h"
        fig.add_trace(
            go.Scatter(
                x=activity_streams["time"].data
                if time
                else activity_streams["distance"].data,
                y=y,
                hovertemplate=hovertemplate,
                line={"color": "#0000FF"},
            )
        )
        return fig

    def create_ele_graph(activity_streams, time):
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=activity_streams["time"].data
                if time
                else activity_streams["distance"].data,
                y=activity_streams["altitude"].data,
                hovertemplate="Time: %{x}<br>Elevation: %{y:.2f} m"
                if time
                else "Distance: %{x} m<br>Elevation: %{y:.2f} m",  # TODO convert to km
                line={"color": "#00FF00"},
            )
        )
        return fig

    def create_heartrate_graph(activity_streams, time):
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=activity_streams["time"].data
                if time
                else activity_streams["distance"].data,
                y=activity_streams["heartrate"].data,
                hovertemplate="Time: %{x}<br>Heartrate: %{y:.2f} bpm"
                if time
                else "Distance: %{x} m<br>Heartrate: %{y:.2f} bpm",
                line={"color": "#FF0000"},
            )
        )
        return fig

    def create_map(activity_streams, color):
        lats = [point[0] for point in activity_streams["latlng"].data]
        lons = [point[1] for point in activity_streams["latlng"].data]
        center_lat = np.mean(lats)
        center_lon = np.mean(lons)

        m = folium.Map([center_lat, center_lon], zoom_start=15)

        colormap = COLORMAPS[color].scale(
            min(activity_streams[color].data), max(activity_streams[color].data)
        )

        folium.ColorLine(
            positions=list(zip(lats, lons)),
            colors=activity_streams[color].data,
            colormap=colormap,
            weight=5,
        ).add_to(m)

        m.add_child(colormap)

        return m.get_root().render()

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
            Output(
                {"page": "activity", "tab": "graphs", "component": "map"},
                "srcDoc",
            ),
        ],
        [
            Input("url", "pathname"),
            Input(
                {
                    "page": "activity",
                    "tab": "graphs",
                    "component": "time-dist-control",
                },
                "value",
            ),
            Input(
                {
                    "page": "activity",
                    "tab": "graphs",
                    "component": "pace-speed-control",
                },
                "value",
            ),
            Input(
                {
                    "page": "activity",
                    "component": "graphs-trace-color-select",
                },
                "value",
            ),
        ],
        State("activities-store", "data"),
    )
    def update_graphs(pathname, time_dist, pace_speed, trace_color, data):
        """
        Update the graphs.
        """
        if pathname is None or "/activity" not in pathname:
            raise PreventUpdate
        if data is None or data == {}:
            raise PreventUpdate

        activity_id = int(pathname.split("/")[-1])

        activity_streams = CLIENT.get_activity_streams(
            activity_id,
            [
                "time",
                "latlng",
                "distance",
                "altitude",
                "velocity_smooth",
                "heartrate",
                "cadence",
                "watts",
                "grade_smooth",
            ],
        )

        return (
            create_speed_graph(
                activity_streams, time_dist == "time", pace_speed == "pace"
            ),
            create_ele_graph(activity_streams, time_dist == "time"),
            create_heartrate_graph(activity_streams, time_dist == "time"),
            create_map(activity_streams, trace_color),
        )
