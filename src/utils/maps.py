"""
This module contains the utilities for maps visualisation.
"""

import plotly.graph_objects as go
import polyline


def create_scattermap(
    polyline_str: str, name: str = "", color: str = "#FFA800"
) -> tuple[go.Scattermap, float, float]:
    """
    Creates a Scattermap object from a polyline string and returns it along with the center coordinates.

    Args:
        polyline_str (str): _description_
        color (str, optional): _description_. Defaults to "#FFA800".

    Returns:
        tuple[go.Scattermap, float, float]: _description_
    """
    decoded_polyline = polyline.decode(polyline_str)

    lat = [point[0] for point in decoded_polyline]
    lon = [point[1] for point in decoded_polyline]

    min_lat, min_lon, max_lat, max_lon = min(lat), min(lon), max(lat), max(lon)
    center_lat = min_lat + (max_lat - min_lat) / 2
    center_lon = min_lon + (max_lon - min_lon) / 2

    return (
        go.Scattermap(
            lat=lat,
            lon=lon,
            name=name,
            mode="lines",
            marker={
                "size": 5,
                "color": color,
            },
        ),
        center_lat,
        center_lon,
    )
