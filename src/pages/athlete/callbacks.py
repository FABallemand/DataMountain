"""
This module contains the callbacks of the Athelete page.
"""

import datetime

import dash_mantine_components as dmc
from dash import Input, Output, callback


def create_location_string(data):
    """
    Create a location string from athlete data.
    """
    location_parts = [data["city"], data["state"], data["country"]]
    location = ", ".join(part for part in location_parts if part)
    return location if location else "-"


def create_clubs_string(data):
    """
    Create a clubs string from athlete data.
    """
    return (
        data["clubs"] if data["clubs"] else "-"
    )  # TODO improve if clubs list is available


def create_totals_table(data):
    """
    Create totals stats table.
    """
    return dmc.Table(
        data={
            "body": [
                [
                    "Activity Count",
                    f"{data['count']}",
                ],
                [
                    "Distance",
                    f"{data['distance'] / 1000:.2f} km",
                ],
                [
                    "Elapsed / Moving Time",
                    f"{data['elapsed_time']:.2f} / {data['moving_time']:.2f}",
                ],
                [
                    "Elevation Gain",
                    f"{data['elevation_gain']:.2f} m",
                ],
            ],
        },
        striped=False,
        highlightOnHover=False,
        withTableBorder=False,
        withColumnBorders=False,
    )


def register_callbacks():
    """
    Register callbacks of the Athelete page.
    """

    @callback(
        Output({"page": "athlete", "component": "athlete-card"}, "children"),
        [
            Input("url", "pathname"),
            Input("athlete-store", "data"),
        ],
    )
    def update_athlete_card(_, data):
        """
        Update the athlete card.
        """
        return dmc.Group(
            [
                dmc.Stack(
                    [
                        dmc.Title(f"{data['firstname']} {data['lastname']}", order=1),
                        dmc.Text(f"Gender: {data['sex']}"),
                        dmc.Text(f"Location: {create_location_string(data)}"),
                        dmc.Text(f"Clubs: {create_clubs_string(data)}"),
                        dmc.Text(f"Following: {data['friend_count']}"),
                        dmc.Text(f"Followers: {data['follower_count']}"),
                    ]
                ),
                dmc.Avatar(src=data["profile"], radius="xl"),
            ],
            justify="space-between",
        )

    @callback(
        Output({"page": "athlete", "component": "stats-card"}, "children"),
        [
            Input("url", "pathname"),
            Input("athlete-store", "data"),
        ],
    )
    def update_stats_card(_, data):
        """
        Update the athlete card.
        """
        return dmc.Group(
            [
                dmc.Stack(
                    [
                        dmc.Title(
                            f"{datetime.datetime.now().date().year} Totals", order=1
                        ),
                        create_totals_table(data["ytd_run_totals"]),
                        create_totals_table(data["ytd_ride_totals"]),
                        create_totals_table(data["ytd_swim_totals"]),
                    ]
                ),
                dmc.Stack(
                    [
                        dmc.Title("Totals", order=1),
                        create_totals_table(data["all_run_totals"]),
                        create_totals_table(data["all_ride_totals"]),
                        create_totals_table(data["all_swim_totals"]),
                    ]
                ),
            ]
        )
