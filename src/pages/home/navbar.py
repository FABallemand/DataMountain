"""
This module contains the layout of the Home page navbar.
"""

import dash_mantine_components as dmc


def HomeNavbar():
    """
    Create the layout of the Home page navbar.
    """
    return [
        dmc.Title("Home", order=1),
        dmc.MultiSelect(
            id={"page": "home", "component": "sport-type-select"},
            label="Sport Type",
            placeholder="Select sport type",
            searchable=True,
            data=[
                {
                    "group": "Cycling",
                    "items": [
                        {
                            "value": "GravelBikeRide",
                            "label": "Gravel Bike",
                        },  # TODO check sport type
                        {"value": "MoutainBikeRide", "label": "Moutain Bike"},
                        {"value": "Ride", "label": "Road Bike"},
                    ],
                },
                {
                    "group": "Running",
                    "items": [
                        {"value": "Run", "label": "Run"},
                        {"value": "TrailRun", "label": "Trail Run"},
                    ],
                },
                {
                    "group": "Walking",
                    "items": [
                        {"value": "Hike", "label": "Hike"},  # TODO check sport type
                        {"value": "Walk", "label": "Walk"},  # TODO check sport type
                    ],
                },
                {
                    "group": "Other",
                    "items": [
                        {"value": "Swim", "label": "Swim"},  # TODO check sport type
                    ],
                },
            ],
            value=["Run", "TrailRun"],
        ),
    ]
