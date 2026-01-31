"""
This module contains the utilities for maps visualisation.
"""

from math import log2

import plotly.graph_objects as go
import polars as pl
import polyline


def compute_map_coords(
    center_lats: list,
    center_lons: list,
    min_lats: list,
    min_lons: list,
    max_lats: list,
    max_lons: list,
    threshold: float = 1.5,
) -> dict[str, float]:
    """
    Compute map reference coordinates (without outliers) for map
    plotting (i.e.: min, max and center coordinates).

    Args:
        center_lats (list): List of center latitudes.
        center_lons (list): List of center longitudes.
        min_lats (list): List of minimum latitudes.
        min_lons (list): List of minimum longitudes.
        max_lats (list): List of maximum latitudes.
        max_lons (list): List of maximum longitudes.
        threshold (float, optional): Z-score threshold used to remove
            outliers. Defaults to 1.5.

    Returns:
        dict[str, float]: Dictionary of reference coordinates for map
            plotting.
    """
    df = (
        pl.DataFrame(
            {
                "center_lats": center_lats,
                "center_lons": center_lons,
                "min_lats": min_lats,
                "min_lons": min_lons,
                "max_lats": max_lats,
                "max_lons": max_lons,
            }
        )
        .with_columns(
            (
                (pl.col("center_lats") - pl.col("center_lats").mean())
                / pl.col("center_lats").std()
            ).alias("z_center_lats"),
            (
                (pl.col("center_lons") - pl.col("center_lons").mean())
                / pl.col("center_lons").std()
            ).alias("z_center_lons"),
        )
        .filter(
            (pl.col("z_center_lats") < threshold)
            & (pl.col("z_center_lons") < threshold)
        )
    )
    return {
        "center_lat": df.get_column("center_lats").mean(),
        "center_lon": df.get_column("center_lons").mean(),
        "min_lat": df.get_column("min_lats").min(),
        "min_lon": df.get_column("min_lons").min(),
        "max_lat": df.get_column("max_lats").max(),
        "max_lon": df.get_column("max_lons").max(),
    }


def _create_scattermap(
    polyline_str: str, name: str = "", color: str = "#FFA800"
) -> tuple[go.Scattermap, dict[str, float]]:
    """
    Create a Scattermap object from a polyline string and return it
    along with the center coordinates.

    Args:
        polyline_str (str): Polyline string representing the path.
        name (str, optional): Name of the trace. Defaults to "".
        color (str, optional): Color of the trace. Defaults to "#FFA800".

    Returns:
        tuple[go.Scattermap, dict[str, float]]: Scattermap object and
            dictionary containting useful coordinates (min, max and
            center latitude and longitude).
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
        {
            "center_lat": center_lat,
            "center_lon": center_lon,
            "min_lat": min_lat,
            "min_lon": min_lon,
            "max_lat": max_lat,
            "max_lon": max_lon,
        },
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

    # Iterate over polylines
    center_lats, center_lons = [], []
    min_lats, min_lons, max_lats, max_lons = [], [], [], []
    for pl_str, n, c in zip(polyline_str, name, color):
        scattermap, coords = _create_scattermap(pl_str, n, c)
        fig.add_trace(scattermap)
        center_lats.append(coords["center_lat"])
        center_lons.append(coords["center_lon"])
        min_lats.append(coords["min_lat"])
        min_lons.append(coords["min_lon"])
        max_lats.append(coords["max_lat"])
        max_lons.append(coords["max_lon"])
    # Remove outliers from coordinates
    map_coords = compute_map_coords(
        center_lats, center_lons, min_lats, min_lons, max_lats, max_lons
    )
    # Compute map zoom
    lat_range = map_coords["max_lat"] - map_coords["min_lat"]
    lon_range = map_coords["max_lon"] - map_coords["min_lon"]
    max_range = max(lat_range, lon_range)
    zoom = 8 - log2(max_range + 1e-6)
    # Update figure layout
    fig.update_layout(
        margin={"l": 0, "t": 0, "b": 0, "r": 0},
        map={
            "center": {
                "lon": map_coords["center_lon"],
                "lat": map_coords["center_lat"],
            },
            "style": map_layer,
            "zoom": zoom,
        },
    )
    return fig
