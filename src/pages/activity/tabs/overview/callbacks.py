"""
This module contains the callbacks of the Overview tab of the Activity page.
"""

import time

import dash_mantine_components as dmc
import ezgpx
import polars as pl
import polyline
from dash import Input, Output, State, callback
from dash.exceptions import PreventUpdate

from constants.colors import SPORT_TYPE_COLORS


def register_callbacks():
    """
    Register callbacks of the Overview tab of the Activity page.
    """

    @callback(
        Output(
            {
                "page": "activity",
                "tab": "overview",
                "component": "graph",
            },
            "figure",
        ),
        Input("url", "pathname"),
        State("activities-store", "data"),
    )
    def update_map(pathname, data):
        """
        Update the map.
        """
        if pathname is None or "/activity" not in pathname:
            raise PreventUpdate
        if data is None or data == {}:
            raise PreventUpdate

        activity_data = pl.DataFrame(data).filter(
            pl.col("id") == int(pathname.split("/")[-1])
        )

        if activity_data.is_empty():
            raise PreventUpdate

        activity_data = activity_data.row(0)

        decoded_polyline = polyline.decode(activity_data[22]["summary_polyline"])
        gpx = ezgpx.GPX()
        trk = ezgpx.gpx_elements.Track()
        trk_seg = ezgpx.gpx_elements.TrackSegment()
        for lat, lon in decoded_polyline:
            trk_seg.trkpt.append(
                ezgpx.gpx_elements.WayPoint(tag="trkpt", lat=lat, lon=lon)
            )
        trk.trkseg.append(trk_seg)
        gpx.gpx.trk.append(trk)
        gpx._time_data = True  # TODO trick for plotting (fix ezgpx?)
        gpx._ele_data = True  # TODO trick for plotting (fix ezgpx?)

        return ezgpx.plotters.PlotlyPlotter(gpx).plot(
            color=SPORT_TYPE_COLORS[activity_data[29]]
        )

    @callback(
        Output(
            {
                "page": "activity",
                "tab": "overview",
                "component": "stats",
            },
            "children",
        ),
        Input("url", "pathname"),
        State("activities-store", "data"),
    )
    def update_stats(pathname, data):
        """
        Update the statistics.
        """
        if pathname is None or "/activity" not in pathname:
            raise PreventUpdate
        if data is None or data == {}:
            raise PreventUpdate

        activity_data = pl.DataFrame(data).filter(
            pl.col("id") == int(pathname.split("/")[-1])
        )

        if activity_data.is_empty():
            raise PreventUpdate

        return [
            dmc.Text(f"Distance: {activity_data['distance'].item() / 1000:.2f} km"),
            dmc.Text(
                f"Total Elevation Gain: {activity_data['total_elevation_gain'].item():.2f} m"
            ),
            dmc.Text(
                f"Elapsed Time: {
                    time.strftime(
                        '%H:%M:%S',
                        time.gmtime(activity_data['elapsed_time'].item()),
                    )
                }"
            ),
            dmc.Text(
                f"Moving Time: {
                    time.strftime(
                        '%H:%M:%S', time.gmtime(activity_data['moving_time'].item())
                    )
                }"
            ),
            dmc.Text(
                f"Average Pace {60 / (activity_data['average_speed'].item() * 3.6):.2f} min/km"
            ),
            dmc.Text(
                f"Average Speed: {activity_data['average_speed'].item() * 3.6:.2f} km/h"
            ),
            dmc.Text(
                f"Average Heartrate: {activity_data['average_heartrate'].item()} bpm"
            ),
        ]
