# pylint: disable=invalid-name
# Disable invalid name to match dash PascalCase
"""
This module contains the layout of the Home page navbar.
"""

import datetime

import dash_mantine_components as dmc
from dash_iconify import DashIconify

from templates.components.selects import SportTypeSelect


def HomeNavbar():
    """
    Create the layout of the Home page navbar.
    """
    return [
        dmc.Title("Home", order=1),
        SportTypeSelect({"page": "home", "component": "sport-type-select"}),
        dmc.DatePickerInput(
            id={"page": "home", "component": "start-date-picker"},
            label="Start Date",
            valueFormat="DD/MM/YYYY",
            value=(
                datetime.datetime.now() - datetime.timedelta(days=30)
            ).date(),  # TODO do something to load more data
            leftSection=DashIconify(icon="ic:baseline-calendar-month"),
        ),
        dmc.DatePickerInput(
            id={"page": "home", "component": "stop-date-picker"},
            label="Stop Date",
            valueFormat="DD/MM/YYYY",
            value=datetime.datetime.now().date(),
            leftSection=DashIconify(icon="ic:baseline-calendar-month"),
        ),
    ]
