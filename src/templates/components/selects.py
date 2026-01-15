# pylint: disable=invalid-name, redefined-builtin
# Disable invalid name to match dash PascalCase
# Disable redefined builtin for id parameter
"""
This module contains template select components.
"""

import dash_mantine_components as dmc
from dash_iconify import DashIconify


def SportTypeSelect(id: str | dict):
    """
    Create a sport type select component.

    Args:
        id (str | dict): Component ID.

    Returns:
        dmc.MultiSelect: Sport type select component.
    """
    return dmc.MultiSelect(
        id=id,
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
                    },
                    {"value": "MountainBikeRide", "label": "Moutain Bike"},
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
                    {"value": "Hike", "label": "Hike"},
                    {"value": "Walk", "label": "Walk"},
                    {
                        "value": "Snowshoe",
                        "label": "Snow Shoe",
                    },
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
    )


def PlotlyMapLayerSelect(id: str | dict):
    """
    Create a layer select component for Plotly maps.

    Args:
        id (str | dict): Component ID.

    Returns:
        dmc.Select: Map layer select component.
    """
    return dmc.Select(
        id=id,
        label="Map Layer",
        placeholder="Select map layer",
        searchable=True,
        data=[
            {"value": "basic", "label": "Basic"},
            {"value": "carto-darkmatter", "label": "Carto Dark Matter"},
            {
                "value": "carto-darkmatter-nolabels",
                "label": "Carto Dark Matter (No Labels)",
            },
            {"value": "carto-positron", "label": "Carto Positron"},
            {
                "value": "carto-positron-nolabels",
                "label": "Carto Positron (No Labels)",
            },
            {"value": "carto-voyager", "label": "Carto Voyager"},
            {
                "value": "carto-voyager-nolabels",
                "label": "Carto Voyager (No Labels)",
            },
            {"value": "dark", "label": "Dark"},
            {"value": "light", "label": "Light"},
            {"value": "open-street-map", "label": "Open Street Map"},
            {"value": "outdoors", "label": "Outdoors"},
            {"value": "satellite", "label": "Satellite"},
            {"value": "satellite-streets", "label": "Satellite Streets"},
            {"value": "streets", "label": "Streets"},
            {"value": "white-bg", "label": "None"},
        ],
        value="open-street-map",
        leftSection=DashIconify(icon="ic:baseline-layers"),
    )


def FoliumMapLayerSelect(id: str | dict):
    """
    Create a layer select component for Folium maps.

    Args:
        id (str | dict): Component ID.

    Returns:
        dmc.Select: Map layer select component.
    """
    return dmc.Select(
        id=id,
        label="Map Layer",
        placeholder="Select map layer",
        searchable=True,
        data=[
            {"value": "OpenStreetMap", "label": "OpenStreetMap"},
            {"value": "Cartodb Positron", "label": "Cartodb Positron"},
            {
                "value": "Cartodb dark_matter",
                "label": "Cartodb dark_matter",
            },
        ],
        value="OpenStreetMap",
        leftSection=DashIconify(icon="ic:baseline-layers"),
    )
