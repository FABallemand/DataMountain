# pylint: disable=invalid-name
# Disable invalid name to match dash PascalCase
"""
This module contains the layout of the Calendar page navbar.
"""

import dash_mantine_components as dmc

from templates.components.selects import SportTypeSelect


def CalendarNavbar():
    """
    Create the layout of the Calendar page navbar.
    """
    return dmc.Stack(
        [
            dmc.Title("Calendar", order=1),
            SportTypeSelect({"page": "calendar", "component": "sport-type-select"}),
        ]
    )
