"""
This module contains the utilities for maps visualisation.
"""

import plotly.graph_objects as go
import polyline


def _create_scattermap(
    polyline_str: str, name: str = "", color: str = "#FFA800"
) -> tuple[go.Scattermap, float, float]:
    """
    Create a Scattermap object from a polyline string and return it
    along with the center coordinates.

    Args:
        polyline_str (str): Polyline string representing the path.
        name (str, optional): Name of the trace. Defaults to "".
        color (str, optional): Color of the trace. Defaults to "#FFA800".

    Returns:
        tuple[go.Scattermap, float, float]: Scattermap object and center coordinates.
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


def create_map(
    polyline_str: str | list,
    name: str | list = None,
    color: str | list = None,
    map_layer: str = "open-street-map",
) -> go.Figure:
    """
    Create a map figure from polyline strings.

    Args:
        polyline_str (str | list): Polyline string(s) representing the trace(s).
        name (str | list, optional): Name(s) of the trace(s). Defaults to None.
        color (str | list, optional): Color(s) of the trace(s). Defaults to None.
        map_layer (str, optional): Map layer style. Defaults to "open-street-map".

    Returns:
        go.Figure: Map Plotly figure object.
    """
    if isinstance(polyline_str, str):
        polyline_str = [polyline_str]
    if name is None:
        name = [""] * len(polyline_str)
    if color is None:
        color = ["#FFA800"] * len(polyline_str)
    if isinstance(name, str):
        name = [name]
    if isinstance(color, str):
        color = [color]

    fig = go.Figure()
    center_lat, center_lon = 0, 0
    for pl_str, n, c in zip(polyline_str, name, color):
        scattermap, lat, lon = _create_scattermap(pl_str, n, c)
        fig.add_trace(scattermap)
        center_lat += lat
        center_lon += lon
    fig.update_layout(
        margin={"l": 0, "t": 0, "b": 0, "r": 0},
        map={
            "center": {
                "lon": center_lon / len(polyline_str),
                "lat": center_lat / len(polyline_str),
            },
            "style": map_layer,
            "zoom": 10,
        },
    )
    return fig
