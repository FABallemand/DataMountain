# pylint: disable=invalid-name
# Disable invalid name to match dash PascalCase
"""
This module contains the layout of the Activity page navbar.
"""

import dash_mantine_components as dmc

from templates.components.selects import MapLayerSelect


def ActivityNavbar():
    """
    Create the layout of the Activity page navbar.
    """
    return [
        dmc.Title("Activity", order=1),
        MapLayerSelect({"page": "activity", "component": "map-layer-select"}),
    ]
