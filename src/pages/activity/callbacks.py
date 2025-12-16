"""
This module contains the callbacks of the Activities page.
"""

import dash_mantine_components as dmc
import ezgpx
import polars as pl
import polyline
from dash import Input, Output, State, callback, dcc
from dash.exceptions import PreventUpdate


def register_callbacks():
    """
    Register callbacks of the Activities page.
    """

    @callback(
        Output(
            {
                "page": "activity",
                "component": "main-container",
            },
            "children",
        ),
        Input("url", "pathname"),
        State("activities-store", "data"),
    )
    def update_activity_layout(pathname, data):
        """
        Update the Activity page layout.
        """
        if pathname is None or "/activity" not in pathname:
            raise PreventUpdate
        if data is None or data == {}:
            raise PreventUpdate

        activity_data = pl.DataFrame(data).filter(
            pl.col("id") == int(pathname.split("/")[-1])
        )

        if activity_data.is_empty():
            return dmc.Stack(
                [
                    dmc.Title(
                        f"Activity with ID {pathname.split('/')[-1]} does not exist...",
                        order=1,
                    ),
                ],
            )

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

        return dmc.Stack(
            [
                dmc.Title(f"{activity_data[26]}", order=1),
                dcc.Graph(figure=ezgpx.plotters.PlotlyPlotter(gpx).plot()),
            ],
        )
