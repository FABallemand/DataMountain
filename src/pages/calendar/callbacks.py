"""
This module contains the callbacks of the Calendar page.
"""

import datetime

import dash_mantine_components as dmc
import polars as pl
from dash import Input, Output, callback
from dash.exceptions import PreventUpdate

from constants.colors import DIFFICULTY_COLORMAP, MONTH_COLORS, SPORT_TYPE_COLORS
from utils.dataframes import create_weekly_df
from utils.dates import iso_weeks_in_year


def register_callbacks():
    """
    Register callbacks of the Calendar page.
    """

    @callback(
        Output({"page": "calendar", "component": "calendar"}, "children"),
        [
            Input("url", "pathname"),
            Input({"page": "calendar", "component": "sport-type-select"}, "value"),
            Input("activities-store", "data"),
        ],
    )
    def update_calendar(_, sport_types, data):
        """
        Update the calendar.
        """
        if sport_types is None or sport_types == []:
            raise PreventUpdate
        if data is None or data == {}:
            raise PreventUpdate

        # Create table head
        head = dmc.TableThead(
            dmc.TableTr(
                [
                    dmc.TableTh("Monday"),
                    dmc.TableTh("Tuesday"),
                    dmc.TableTh("Wednesday"),
                    dmc.TableTh("Thursday"),
                    dmc.TableTh("Friday"),
                    dmc.TableTh("Saturday"),
                    dmc.TableTh("Sunday"),
                    dmc.TableTh("Weekly Total"),
                ]
            )
        )

        # Create dataframe from data
        df = (
            pl.DataFrame(data)
            .select(
                [
                    "id",
                    "type",
                    "sport_type",
                    "start_date_local",
                    "distance",
                    "elapsed_time",
                    "total_elevation_gain",
                ]
            )
            .filter(pl.col("sport_type").is_in(sport_types))
            .with_columns(
                pl.col("start_date_local").str.to_datetime("%Y-%m-%dT%H:%M:%S+00:00")
            )
            .with_columns(
                pl.col("start_date_local").dt.iso_year().alias("iso_year"),
                pl.col("start_date_local").dt.week().alias("iso_week"),
                pl.col("start_date_local").dt.weekday().alias("weekday"),
            )
        )

        # Create weekly dataframe
        tmp = (
            create_weekly_df(
                pl.DataFrame(data),
                sport_types,
                start_date=df.get_column("start_date_local").min().date(),
                stop_date=df.get_column("start_date_local").max().date()
                + datetime.timedelta(days=1),  # Include last day
            )
            .group_by(["iso_year", "iso_week", "type"])
            .agg(
                [
                    pl.col("distance").sum(),
                    pl.col("elapsed_time").sum(),
                    pl.col("total_elevation_gain").sum(),
                ]
            )
        )
        weekly_df = pl.concat(
            [
                tmp,
                tmp.group_by("iso_year", "iso_week")
                .sum()
                .with_columns(pl.col("type").fill_null(pl.lit("Total"))),
            ]
        )

        # Scale difficulty colormap based on weekly distance
        weekly_max_dist = (
            weekly_df.filter(pl.col("type") == "Total").get_column("distance").max()
        )
        weekly_difficulty_colormap = DIFFICULTY_COLORMAP.scale(0, weekly_max_dist)

        body_children = []
        # Iterate over ISO years
        for iso_year in range(
            df.get_column("iso_year").max(), df.get_column("iso_year").min() - 1, -1
        ):
            df_year = df.filter(pl.col("iso_year") == iso_year)
            # Iterate over ISO calendar weeks
            last_week = (
                df_year.get_column("iso_week").max()
                if iso_year == df.get_column("iso_year").max()
                else iso_weeks_in_year(iso_year)
            )
            first_week = (
                df_year.get_column("iso_week").min()
                if iso_year == df.get_column("iso_year").min()
                else 0
            )
            for iso_week in range(last_week, first_week, -1):
                df_week = df_year.filter(pl.col("iso_week") == iso_week)
                if df_week.height == 0:
                    body_children.append(
                        dmc.TableTr(
                            [
                                dmc.TableTd(
                                    "",
                                    bg=MONTH_COLORS[
                                        datetime.datetime.fromisocalendar(
                                            iso_year, iso_week, 1
                                        ).month
                                    ],
                                ),
                                dmc.TableTd(
                                    "",
                                    bg=MONTH_COLORS[
                                        datetime.datetime.fromisocalendar(
                                            iso_year, iso_week, 2
                                        ).month
                                    ],
                                ),
                                dmc.TableTd(
                                    "",
                                    bg=MONTH_COLORS[
                                        datetime.datetime.fromisocalendar(
                                            iso_year, iso_week, 3
                                        ).month
                                    ],
                                ),
                                dmc.TableTd(
                                    "",
                                    bg=MONTH_COLORS[
                                        datetime.datetime.fromisocalendar(
                                            iso_year, iso_week, 4
                                        ).month
                                    ],
                                ),
                                dmc.TableTd(
                                    "",
                                    bg=MONTH_COLORS[
                                        datetime.datetime.fromisocalendar(
                                            iso_year, iso_week, 5
                                        ).month
                                    ],
                                ),
                                dmc.TableTd(
                                    "",
                                    bg=MONTH_COLORS[
                                        datetime.datetime.fromisocalendar(
                                            iso_year, iso_week, 6
                                        ).month
                                    ],
                                ),
                                dmc.TableTd(
                                    "",
                                    bg=MONTH_COLORS[
                                        datetime.datetime.fromisocalendar(
                                            iso_year, iso_week, 7
                                        ).month
                                    ],
                                ),
                                dmc.TableTd(
                                    f"Calendar Week {iso_week}", bg="lightgray"
                                ),
                            ]
                        )
                    )
                else:
                    row_children = []
                    # Iterate over weekdays
                    for weekday in range(1, 8):
                        df_day = df_week.filter(pl.col("weekday") == weekday)
                        if df_day.height == 0:
                            row_children.append(
                                dmc.TableTd(
                                    "",
                                    bg=MONTH_COLORS[
                                        datetime.datetime.fromisocalendar(
                                            iso_year, iso_week, weekday
                                        ).month
                                    ],
                                )
                            )
                        else:
                            day_children = []
                            for activity in df_day.iter_rows(named=True):
                                color = SPORT_TYPE_COLORS.get(
                                    activity["sport_type"], "gray"
                                )
                                distance_km = activity["distance"] / 1000
                                day_children.append(
                                    dmc.Anchor(
                                        dmc.Badge(
                                            f"{activity['sport_type']}: {distance_km:.2f} km",
                                            color=color,
                                            variant="filled",
                                            style={"margin": "2px"},
                                        ),
                                        href=f"/datamountain/activity/{activity['id']}",
                                    )
                                )
                            row_children.append(
                                dmc.TableTd(
                                    day_children,
                                    bg=MONTH_COLORS[
                                        datetime.datetime.fromisocalendar(
                                            iso_year, iso_week, weekday
                                        ).month
                                    ],
                                )
                            )
                    weekly_running_dist = (
                        weekly_df.filter(
                            (pl.col("type") == "Run")
                            & (pl.col("iso_year") == iso_year)
                            & (pl.col("iso_week") == iso_week)
                        )
                        .get_column("distance")
                        .item()
                        if any(x in ["Run", "TrailRun"] for x in sport_types)
                        else 0.0
                    )
                    weekly_cycling_dist = (
                        weekly_df.filter(
                            (pl.col("type") == "Ride")
                            & (pl.col("iso_year") == iso_year)
                            & (pl.col("iso_week") == iso_week)
                        )
                        .get_column("distance")
                        .item()
                        if any(
                            x in ["Ride", "MountainBikeRide", "GravelBikeRide"]
                            for x in sport_types
                        )
                        else 0.0
                    )
                    weekly_total_dist = (
                        weekly_df.filter(
                            (pl.col("type") == "Total")
                            & (pl.col("iso_year") == iso_year)
                            & (pl.col("iso_week") == iso_week)
                        )
                        .get_column("distance")
                        .item()
                        if len(sport_types) > 0
                        else 0.0
                    )
                    row_children.append(
                        dmc.TableTd(
                            dmc.Stack(
                                [
                                    dmc.Text(f"Calendar Week {iso_week}"),
                                    dmc.Text(f"Running: {weekly_running_dist:.2f} km"),
                                    dmc.Text(f"Cycling: {weekly_cycling_dist:.2f} km"),
                                    dmc.Text(f"Total: {weekly_total_dist:.2f} km"),
                                ]
                            ),
                            bg=weekly_difficulty_colormap(
                                weekly_total_dist
                            ),  # TODO find better way to measure difficulty (activity coefficients, elevation gain...)
                        )
                    )
                    body_children.append(dmc.TableTr(row_children))

        # Create table body
        body = dmc.TableTbody(body_children)

        return [head, body]
