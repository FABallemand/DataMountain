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
    return dmc.Stack(
        [
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
                            dmc.SegmentedControl(
                                id={
                                    "page": "activity",
                                    "tab": "graphs",
                                    "component": "time-dist-control",
                                },
                                data=[
                                    {"value": "time", "label": "Time"},
                                    {"value": "dist", "label": "Distance"},
                                ],
                                value="time",
                                size="sm",
                                radius="md",
                                orientation="horizontal",
                                fullWidth=True,
                                transitionDuration=100,
                                transitionTimingFunction="linear",
                            ),
                            dmc.SegmentedControl(
                                id={
                                    "page": "activity",
                                    "tab": "graphs",
                                    "component": "pace-speed-control",
                                },
                                data=[
                                    {"value": "pace", "label": "Pace"},
                                    {"value": "speed", "label": "Speed"},
                                ],
                                value="pace",
                                size="sm",
                                radius="md",
                                orientation="horizontal",
                                fullWidth=True,
                                transitionDuration=100,
                                transitionTimingFunction="linear",
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
                                    {
                                        "value": "velocity_smooth",
                                        "label": "Speed / Pace",
                                    },
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
    )
