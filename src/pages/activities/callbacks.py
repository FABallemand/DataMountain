"""
This module contains the callbacks of the Activities page.
"""

import dash_mantine_components as dmc
import polars as pl
from dash import Input, Output, callback, dcc
from dash.exceptions import PreventUpdate

from constants.colors import SPORT_TYPE_COLORS
from utils.maps import create_map


def register_callbacks():
    """
    Register callbacks of the Activities page.
    """

    # @callback(
    #     Output({"page": "activities", "component": "activities-table"}, "rowData"),
    #     [
    #         Input("url", "pathname"),
    #         Input("activities-store", "data"),
    #     ],
    # )
    # def update_activities_table(pathname, data):
    #     """
    #     Update the activities table.
    #     """
    #     if pathname is None or "/activities" not in pathname:
    #         raise PreventUpdate
    #     if data is None or data == {}:
    #         raise PreventUpdate

    #     return data

    @callback(
        Output({"page": "activities", "component": "activities-list"}, "children"),
        [
            Input("url", "pathname"),
            Input({"page": "activities", "component": "map-layer-select"}, "value"),
            Input("activities-store", "data"),
        ],
    )
    def update_activities_list(pathname, map_layer, data):
        """
        Update the activities list.
        """
        if pathname is None or "/activities" not in pathname:
            raise PreventUpdate
        if data is None or data == {}:
            raise PreventUpdate

        activities = []
        for row in pl.DataFrame(data).iter_rows():
            activities.append(
                dmc.Card(
                    children=[
                        dmc.CardSection(
                            dcc.Graph(
                                figure=create_map(
                                    polyline_str=row[22]["summary_polyline"],
                                    name=row[26],
                                    color=SPORT_TYPE_COLORS.get(row[29], "#FFA800"),
                                    map_layer=map_layer,
                                ).update_traces(hoverinfo="skip", hovertemplate=None),
                                config={"scrollZoom": False},  # "displayModeBar": False
                            )
                        ),
                        dmc.Space(h=60),
                        dmc.Stack(
                            [
                                dmc.Badge(row[29], color=SPORT_TYPE_COLORS[row[29]]),
                                dmc.Title(row[26], order=3),
                                dmc.Anchor(
                                    dmc.Button(
                                        "Go to report",
                                        fullWidth=True,
                                        radius="md",
                                    ),
                                    href=f"/datamountain/activity/{row[0]}",
                                    mt="auto",  # Push button to the bottom of the card
                                ),
                            ],
                            flex=1,
                        ),
                    ],
                    withBorder=True,
                    shadow="sm",
                    radius="md",
                    style={
                        "display": "flex",
                        "flexDirection": "column",
                        "height": "100%",
                    },
                )
            )

        return activities
