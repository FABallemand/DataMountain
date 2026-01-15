# pylint: disable=invalid-name
# Disable invalid name to match dash PascalCase
"""
This module contains the layout of the Map page navbar.
"""

import datetime

import dash_mantine_components as dmc
from dash_iconify import DashIconify

from templates.components.selects import MapLayerSelect, SportTypeSelect


def MapNavbar():
    """
    Create the layout of the Map page navbar.
    """
    return [
        dmc.Title("Map", order=1),
        SportTypeSelect({"page": "map", "component": "sport-type-select"}),
        dmc.DatePickerInput(
            id={"page": "map", "component": "start-date-picker"},
            label="Start Date",
            valueFormat="DD/MM/YYYY",
            value=(
                datetime.datetime.now() - datetime.timedelta(days=30)
            ).date(),  # TODO do something to load more data
            leftSection=DashIconify(icon="ic:baseline-calendar-month"),
        ),
        dmc.DatePickerInput(
            id={"page": "map", "component": "stop-date-picker"},
            label="Stop Date",
            valueFormat="DD/MM/YYYY",
            value=datetime.datetime.now().date(),
            leftSection=DashIconify(icon="ic:baseline-calendar-month"),
        ),
        MapLayerSelect({"page": "map", "component": "map-layer-select"}),
    ]
