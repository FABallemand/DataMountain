"""
This module contains the callbacks of the Activities page.
"""

import dash_mantine_components as dmc
import ezgpx
import polars as pl
import polyline
from dash import Input, Output, callback, dcc
from dash.exceptions import PreventUpdate


def register_callbacks():
    """
    Register callbacks of the Activities page.
    """

    @callback(
        Output({"page": "activities", "component": "activities-table"}, "rowData"),
        [
            Input("url", "pathname"),
            Input("activities-store", "data"),
        ],
    )
    def update_activities_table(pathname, data):
        """
        Update the activities table.
        """
        if pathname is None or "/activities" not in pathname:
            raise PreventUpdate
        if data is None or data == {}:
            raise PreventUpdate

        return data

    @callback(
        Output({"page": "activities", "component": "activities-list"}, "children"),
        [
            Input("url", "pathname"),
            Input("activities-store", "data"),
        ],
    )
    def update_activities_list(pathname, data):
        """
        Update the activities list.
        """
        if pathname is None or "/activities" not in pathname:
            raise PreventUpdate
        if data is None or data == {}:
            raise PreventUpdate

        activities = []
        for row in pl.DataFrame(data).iter_rows():
            decoded_polyline = polyline.decode(row[22]["summary_polyline"])
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
            activities.append(
                dmc.Card(
                    children=[
                        dmc.CardSection(
                            dcc.Graph(
                                figure=ezgpx.plotters.PlotlyPlotter(gpx).plot(),
                                config={"scrollZoom": False},  # "displayModeBar": False
                            )
                        ),
                        dmc.Group(
                            [
                                dmc.Text(row[26], fw=500),
                                dmc.Badge(row[29], color="pink"),
                            ],
                            justify="space-between",
                            mt="md",
                            mb="xs",
                        ),
                        dmc.Text(
                            "Description?",
                            size="sm",
                            c="dimmed",
                        ),
                        dcc.Link(
                            dmc.Text("Go to report", size="lg"),
                            href=f"/datamountain/activity/{row[0]}",
                            style={"textDecoration": "none"},
                        ),
                    ],
                    withBorder=True,
                    shadow="sm",
                    radius="md",
                )
            )

        return activities
