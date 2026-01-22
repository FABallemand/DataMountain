"""
This module contains the callbacks of the Athelete page.
"""

import datetime
import time

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


def create_activity_totals_rows(data, activity):
    """
    Create totals rows for a given activity ("run", "ride", "swim").
    """
    return [
        dmc.TableTr(
            [
                dmc.TableTd("Activity Count"),
                dmc.TableTd(f"{data[f'recent_{activity}_totals']['count']}"),
                dmc.TableTd(f"{data[f'ytd_{activity}_totals']['count']}"),
                dmc.TableTd(f"{data[f'all_{activity}_totals']['count']}"),
            ]
        ),
        dmc.TableTr(
            [
                dmc.TableTd("Distance"),
                dmc.TableTd(
                    f"{data[f'recent_{activity}_totals']['distance'] / 1000:.2f} km"
                ),
                dmc.TableTd(
                    f"{data[f'ytd_{activity}_totals']['distance'] / 1000:.2f} km"
                ),
                dmc.TableTd(
                    f"{data[f'all_{activity}_totals']['distance'] / 1000:.2f} km"
                ),
            ]
        ),
        dmc.TableTr(
            [
                dmc.TableTd(
                    "Moving / Elapsed Time",
                ),
                dmc.TableTd(
                    time.strftime(
                        "%H:%M:%S",
                        time.gmtime(data[f"recent_{activity}_totals"]["moving_time"]),
                    )
                    + " / "
                    + time.strftime(
                        "%H:%M:%S",
                        time.gmtime(data[f"recent_{activity}_totals"]["elapsed_time"]),
                    )
                ),
                dmc.TableTd(
                    time.strftime(
                        "%H:%M:%S",
                        time.gmtime(data[f"ytd_{activity}_totals"]["moving_time"]),
                    )
                    + " / "
                    + time.strftime(
                        "%H:%M:%S",
                        time.gmtime(data[f"ytd_{activity}_totals"]["elapsed_time"]),
                    )
                ),
                dmc.TableTd(
                    time.strftime(
                        "%H:%M:%S",
                        time.gmtime(data[f"all_{activity}_totals"]["moving_time"]),
                    )
                    + " / "
                    + time.strftime(
                        "%H:%M:%S",
                        time.gmtime(data[f"all_{activity}_totals"]["elapsed_time"]),
                    )
                ),
            ]
        ),
        dmc.TableTr(
            [
                dmc.TableTd("Elevation Gain"),
                dmc.TableTd(
                    f"{data[f'recent_{activity}_totals']['elevation_gain']:.2f} m"
                ),
                dmc.TableTd(
                    f"{data[f'ytd_{activity}_totals']['elevation_gain']:.2f} m"
                ),
                dmc.TableTd(
                    f"{data[f'all_{activity}_totals']['elevation_gain']:.2f} m"
                ),
            ]
        ),
    ]


def create_totals_table(data):
    """
    Create table of totals.
    """
    return dmc.Table(
        children=[
            # Table head
            dmc.TableThead(
                dmc.TableTr(
                    [
                        dmc.TableTh(""),
                        dmc.TableTh("Recent"),
                        dmc.TableTh(f"{datetime.datetime.now().date().year}"),
                        dmc.TableTh("All Time"),
                    ]
                )
            ),
            # Table body
            dmc.TableTbody(
                [
                    dmc.TableTr(
                        dmc.TableTd(
                            "Running", bg="lightgray", tableProps={"colSpan": 4}
                        )
                    ),
                    *create_activity_totals_rows(data, "run"),
                    dmc.TableTr(
                        dmc.TableTd(
                            "Cycling", bg="lightgray", tableProps={"colSpan": 4}
                        )
                    ),
                    *create_activity_totals_rows(data, "ride"),
                    dmc.TableTr(
                        dmc.TableTd(
                            "Swimming", bg="lightgray", tableProps={"colSpan": 4}
                        )
                    ),
                    *create_activity_totals_rows(data, "swim"),
                ]
            ),
        ],
        striped=False,
        highlightOnHover=True,
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
        Update the stats card.
        """
        return dmc.Stack(
            [
                dmc.Title("Totals", order=1),
                create_totals_table(data),
            ]
        )

    @callback(
        Output({"page": "athlete", "component": "gear-card"}, "children"),
        [
            Input("url", "pathname"),
            Input("athlete-store", "data"),
        ],
    )
    def update_gear_card(_, data):
        """
        Update the gear card.
        """
        return dmc.Stack(
            [
                dmc.Title("Gear", order=1),
                dmc.Table(
                    children=[
                        # Table head
                        dmc.TableThead(
                            dmc.TableTr(
                                [
                                    dmc.TableTh("Name"),
                                    dmc.TableTh("Distance"),
                                ]
                            )
                        ),
                        # Table body
                        dmc.TableTbody(
                            [
                                dmc.TableTr(
                                    dmc.TableTd(
                                        "Shoes",
                                        bg="lightgray",
                                        tableProps={"colSpan": 2},
                                    )
                                ),
                                *[
                                    dmc.TableTr(
                                        [
                                            dmc.TableTd(shoe["name"]),
                                            dmc.TableTd(
                                                f"{shoe['distance'] / 1000:.2f} km"
                                            ),
                                        ]
                                    )
                                    for shoe in sorted(
                                        data["shoes"],
                                        reverse=True,
                                        key=lambda item: item["distance"],
                                    )
                                ],
                                dmc.TableTr(
                                    dmc.TableTd(
                                        "Bikes",
                                        bg="lightgray",
                                        tableProps={"colSpan": 2},
                                    )
                                ),
                                *[
                                    dmc.TableTr(
                                        [
                                            dmc.TableTd(bike["name"]),
                                            dmc.TableTd(
                                                f"{bike['distance'] / 1000:.2f} km"
                                            ),
                                        ]
                                    )
                                    for bike in sorted(
                                        data["bikes"],
                                        reverse=True,
                                        key=lambda item: item["distance"],
                                    )
                                ],
                            ]
                        ),
                    ],
                    striped=False,
                    highlightOnHover=True,
                    withTableBorder=False,
                    withColumnBorders=False,
                ),
            ]
        )
