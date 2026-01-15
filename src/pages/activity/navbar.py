# pylint: disable=invalid-name
# Disable invalid name to match dash PascalCase
"""
This module contains the layout of the Activity page navbar.
"""

import dash_mantine_components as dmc

from templates.components.selects import FoliumMapLayerSelect, PlotlyMapLayerSelect


def ActivityNavbar():
    """
    Create the layout of the Activity page navbar.
    """
    return [
        dmc.Title("Activity", order=1),
        dmc.Fieldset(
            [
                PlotlyMapLayerSelect(
                    {
                        "page": "activity",
                        "component": "overview-map-layer-select",
                    }
                ),
            ],
            legend="Overview",
            variant="filled",
            radius="md",
        ),
        dmc.Fieldset(
            [
                dmc.Stack(
                    [
                        dmc.Switch(
                            id={
                                "page": "activity",
                                "tab": "graphs",
                                "component": "time-dist-switch",
                            },
                            offLabel="Time",
                            onLabel="Distance",
                            checked="False",
                            size="lg",
                        ),
                        dmc.Switch(
                            id={
                                "page": "activity",
                                "tab": "graphs",
                                "component": "pace-speed-switch",
                            },
                            offLabel="Pace",
                            onLabel="Speed",
                            checked="False",
                            size="lg",
                        ),
                        FoliumMapLayerSelect(
                            {
                                "page": "activity",
                                "component": "graphs-map-layer-select",
                            }
                        ),
                        dmc.Select(
                            id={
                                "page": "activity",
                                "component": "graphs-trace-color-select",
                            },
                            label="Trace Color",
                            placeholder="Select trace color",
                            searchable=True,
                            data=[
                                {"value": "distance", "label": "Distance"},
                                {"value": "altitude", "label": "Elevation"},
                                {"value": "velocity_smooth", "label": "Speed / Pace"},
                                {"value": "heartrate", "label": "Heart Rate"},
                                {"value": "cadence", "label": "Cadence"},
                                {"value": "watts", "label": "Power"},
                                {"value": "grade_smooth", "label": "Grade (???)"},
                            ],
                            value="altitude",
                        ),
                    ]
                ),
            ],
            legend="Graphs",
            variant="filled",
            radius="md",
        ),
    ]
