# pylint: disable=invalid-name
# Disable invalid name to match dash PascalCase
"""
This module contains the layout of the Activities page navbar.
"""

import dash_mantine_components as dmc

from templates.components.selects import PlotlyMapLayerSelect


def ActivitiesNavbar():
    """
    Create the layout of the Activities page navbar.
    """
    return dmc.Stack(
        [
            dmc.Title("Activities", order=1),
            PlotlyMapLayerSelect(
                {"page": "activities", "component": "map-layer-select"}
            ),
        ]
    )
