"""
This module contains the callbacks of the Overview tab of the Activity page.
"""

import time

import polars as pl
from dash import Input, Output, State, callback
from dash.exceptions import PreventUpdate


def register_callbacks():
    """
    Register callbacks of the Overview tab of the Activity page.
    """

    def create_stat(value, unit):
        if value is None:
            return ""
        if isinstance(value, float):
            return f"{value:.2f} {unit}"
        return f"{value} {unit}"

    @callback(
        [
            Output(
                {
                    "page": "activity",
                    "tab": "statistics",
                    "component": "general-table",
                },
                "data",
            ),
            Output(
                {
                    "page": "activity",
                    "tab": "statistics",
                    "component": "perf-table",
                },
                "data",
            ),
            Output(
                {
                    "page": "activity",
                    "tab": "statistics",
                    "component": "gear-table",
                },
                "data",
            ),
            Output(
                {
                    "page": "activity",
                    "tab": "statistics",
                    "component": "location-table",
                },
                "data",
            ),
            Output(
                {
                    "page": "activity",
                    "tab": "statistics",
                    "component": "time-table",
                },
                "data",
            ),
            Output(
                {
                    "page": "activity",
                    "tab": "statistics",
                    "component": "strava-table",
                },
                "data",
            ),
        ],
        Input("url", "pathname"),
        State("activities-store", "data"),
    )
    def update_tables(pathname, data):
        """
        Update the statistics tables.
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
            {
                "body": [
                    ["Type", activity_data["type"].item()],
                    ["Sport Type", activity_data["sport_type"].item()],
                    ["Workout Type", activity_data["workout_type"].item()],
                    ["Trainer", str(activity_data["trainer"].item())],
                    ["Commute", str(activity_data["commute"].item())],
                ],
            },
            {
                "body": [
                    [
                        "Distance",
                        create_stat(activity_data["distance"].item() / 1000, "km"),
                    ],
                    [
                        "Total Elevation Gain",
                        create_stat(activity_data["total_elevation_gain"].item(), "m"),
                    ],
                    [
                        "Elapsed Time",
                        time.strftime(
                            "%H:%M:%S",
                            time.gmtime(activity_data["elapsed_time"].item()),
                        ),
                    ],
                    [
                        "Moving Time",
                        time.strftime(
                            "%H:%M:%S", time.gmtime(activity_data["moving_time"].item())
                        ),
                    ],
                    [
                        "Average Pace",
                        create_stat(
                            60 / (activity_data["average_speed"].item() * 3.6), "min/km"
                        ),
                    ],
                    [
                        "Max Pace",
                        create_stat(
                            60 / (activity_data["max_speed"].item() * 3.6), "min/km"
                        ),
                    ],
                    [
                        "Average Speed",
                        create_stat(
                            activity_data["average_speed"].item() * 3.6, "km/h"
                        ),
                    ],
                    [
                        "Max Speed",
                        create_stat(activity_data["max_speed"].item() * 3.6, "km/h"),
                    ],
                    ["Average Cadence", activity_data["average_cadence"].item()],
                    [
                        "Average Heartrate",
                        create_stat(activity_data["average_heartrate"].item(), "bpm"),
                    ],
                    [
                        "Max Heartrate",
                        create_stat(activity_data["max_heartrate"].item(), "bpm"),
                    ],
                    [
                        "Average Watts",
                        create_stat(activity_data["average_watts"].item(), "W"),
                    ],
                    [
                        "Weighted Average Watts",
                        create_stat(
                            activity_data["weighted_average_watts"].item(), "W"
                        ),
                    ],
                    [
                        "Max Watts",
                        create_stat(activity_data["max_watts"].item(), "W"),
                    ],
                    [
                        "Device Watts",
                        create_stat(activity_data["device_watts"].item(), "W"),
                    ],
                    ["Kilojoules", activity_data["kilojoules"].item()],
                    ["Suffer Score", activity_data["suffer_score"].item()],
                ]
            },
            {
                "body": [
                    ["Gear ID", activity_data["gear_id"].item()],
                ]
            },
            {
                "body": [
                    ["Location City", activity_data["location_city"].item()],
                    ["Location State", activity_data["location_state"].item()],
                    ["Location Country", activity_data["location_country"].item()],
                    [
                        "Start Coordinates",
                        activity_data["start_latlng"].item().to_list(),
                    ],
                    ["End Coordinates", activity_data["end_latlng"].item().to_list()],
                    ["Elevation Low", activity_data["elev_low"].item()],
                    ["Elevation High", activity_data["elev_high"].item()],
                ]
            },
            {
                "body": [
                    ["Start Date", activity_data["start_date"].item()],
                    ["Start Date Local", activity_data["start_date_local"].item()],
                    ["Timezone", activity_data["timezone"].item()],
                    ["UTC Offset", activity_data["utc_offset"].item()],
                ]
            },
            {
                "body": [
                    ["Activity ID", activity_data["id"].item()],
                    ["Private", str(activity_data["private"].item())],
                    ["Visibility", activity_data["visibility"].item()],
                    ["Athlete Count", activity_data["athlete_count"].item()],
                    ["Kudos Count", activity_data["kudos_count"].item()],
                    ["Comment Count", activity_data["comment_count"].item()],
                    ["Achievements Count", activity_data["achievement_count"].item()],
                    ["PR Count", activity_data["pr_count"].item()],
                    ["Photo Count", activity_data["photo_count"].item()],
                    ["Total Photo Count", activity_data["total_photo_count"].item()],
                ]
            },
        ]
