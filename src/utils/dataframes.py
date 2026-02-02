"""
This module contains the utilities for dataframes.
"""

import datetime

import polars as pl

from utils.dates import monday_of_week


def create_iso_week_df(
    start_date: datetime.date,
    stop_date: datetime.date,
) -> pl.DataFrame:
    """
    Create dataframe of ISO weeks.

    Args:
        start_date (datetime.date): Start date.
        stop_date (datetime.date): Stop date.

    Returns:
        pl.DataFrame: ISO week dataframe.

    Example:
        >>> create_iso_week_df(datetime.date(2025, 12, 15), datetime.date(2026, 1, 15))
        shape: (5, 2)
        ┌──────────┬──────────┐
        │ iso_year ┆ iso_week │
        │ ---      ┆ ---      │
        │ i32      ┆ i8       │
        ╞══════════╪══════════╡
        │ 2025     ┆ 51       │
        │ 2025     ┆ 52       │
        │ 2026     ┆ 1        │
        │ 2026     ┆ 2        │
        │ 2026     ┆ 3        │
        └──────────┴──────────┘
    """
    return (
        pl.date_range(
            monday_of_week(start_date),
            monday_of_week(stop_date),
            interval="1w",
            eager=True,
        )
        .to_frame("date")
        .with_columns(
            pl.col("date").dt.iso_year().alias("iso_year"),
            pl.col("date").dt.week().alias("iso_week"),
        )
        .drop("date")
        .unique()
        .sort(["iso_year", "iso_week"])
    )


def create_weekly_df(
    df: pl.DataFrame,
    sport_types: list,
    start_date: datetime.date,
    stop_date: datetime.date,
) -> pl.DataFrame:
    """
    Create a weekly dataframe from the activities dataframe.

    Args:
        df (pl.DataFrame): Activities dataframe.
        sport_types (list): List of sport types to keep.
        start_date (datetime.date): Start date.
        stop_date (datetime.date): Stop date.

    Returns:
        pl.DataFrame: Weekly dataframe.
    """
    # Create dataframe from data
    df = (
        df.select(
            [
                "type",
                "sport_type",
                "start_date_local",
                "distance",
                "elapsed_time",
                "total_elevation_gain",
            ]
        )
        .with_columns(
            pl.col("start_date_local").str.to_datetime("%Y-%m-%dT%H:%M:%S+00:00")
        )
        .filter(
            (pl.col("sport_type").is_in(sport_types))
            & (pl.col("start_date_local").is_between(start_date, stop_date))
        )
    )

    # Aggregate distances by week and sport type
    weekly_df = (
        df.with_columns(
            pl.col("start_date_local").dt.iso_year().alias("iso_year"),
            pl.col("start_date_local").dt.week().alias("iso_week"),
        )
        .group_by(["iso_year", "iso_week", "type", "sport_type"])
        .agg(
            [
                pl.col("distance").sum() / 1000,  # Convert to km
                pl.col("elapsed_time").sum() / 60,  # Convert to minutes
                pl.col("total_elevation_gain").sum(),
            ]
        )
    )

    # Create calendar of weeks
    iso_week_df = create_iso_week_df(start_date, stop_date)

    # Retrieve sports types
    sports_df = weekly_df.select(["type", "sport_type"]).unique()

    # Create full index of year_week and sport_type
    full_index = iso_week_df.join(sports_df, how="cross")

    # Merge with weekly_df to fill missing weeks/sport types with 0 distance
    return full_index.join(
        weekly_df, on=["iso_year", "iso_week", "type", "sport_type"], how="left"
    ).with_columns(
        pl.col("distance").fill_null(0),
        pl.col("elapsed_time").fill_null(0),
        pl.col("total_elevation_gain").fill_null(0),
    )
