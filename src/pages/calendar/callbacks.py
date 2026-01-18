"""
This module contains the callbacks of the Calendar page.
"""

import datetime

import dash_mantine_components as dmc
import polars as pl
from dash import Input, Output, callback
from dash.exceptions import PreventUpdate

from constants.colors import MONTH_COLORS, SPORT_TYPE_COLORS


def iso_weeks_in_year(year: int) -> int:
    """
    Return number of ISO calendar weeks in a given year.
    """
    return datetime.date(year, 12, 28).isocalendar().week


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
                pl.col("start_date_local").dt.week().alias("week"),
                pl.col("start_date_local").dt.weekday().alias("weekday"),
            )
        )

        body_children = []
        # Iterate over ISO years
        for iso_year in range(
            df.get_column("iso_year").max(), df.get_column("iso_year").min() - 1, -1
        ):
            df_year = df.filter(pl.col("iso_year") == iso_year)
            # Iterate over ISO calendar weeks
            last_week = (
                df_year.get_column("week").max()
                if iso_year == df.get_column("iso_year").max()
                else iso_weeks_in_year(iso_year)
            )
            first_week = (
                df_year.get_column("week").min()
                if iso_year == df.get_column("iso_year").min()
                else 0
            )
            for week in range(last_week, first_week, -1):
                df_week = df_year.filter(pl.col("week") == week)
                if df_week.height == 0:
                    body_children.append(
                        dmc.TableTr(
                            [
                                dmc.TableTd(
                                    "",
                                    bg=MONTH_COLORS[
                                        datetime.datetime.fromisocalendar(
                                            iso_year, week, 1
                                        ).month
                                    ],
                                ),
                                dmc.TableTd(
                                    "",
                                    bg=MONTH_COLORS[
                                        datetime.datetime.fromisocalendar(
                                            iso_year, week, 2
                                        ).month
                                    ],
                                ),
                                dmc.TableTd(
                                    "",
                                    bg=MONTH_COLORS[
                                        datetime.datetime.fromisocalendar(
                                            iso_year, week, 3
                                        ).month
                                    ],
                                ),
                                dmc.TableTd(
                                    "",
                                    bg=MONTH_COLORS[
                                        datetime.datetime.fromisocalendar(
                                            iso_year, week, 4
                                        ).month
                                    ],
                                ),
                                dmc.TableTd(
                                    "",
                                    bg=MONTH_COLORS[
                                        datetime.datetime.fromisocalendar(
                                            iso_year, week, 5
                                        ).month
                                    ],
                                ),
                                dmc.TableTd(
                                    "",
                                    bg=MONTH_COLORS[
                                        datetime.datetime.fromisocalendar(
                                            iso_year, week, 6
                                        ).month
                                    ],
                                ),
                                dmc.TableTd(
                                    "",
                                    bg=MONTH_COLORS[
                                        datetime.datetime.fromisocalendar(
                                            iso_year, week, 7
                                        ).month
                                    ],
                                ),
                                dmc.TableTd(f"Calendar Week {week}", bg="lightgray"),
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
                                            iso_year, week, weekday
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
                                    dmc.Badge(
                                        f"{activity['sport_type'].capitalize()}: {distance_km:.2f} km",
                                        color=color,
                                        variant="filled",
                                        style={"margin": "2px"},
                                    )
                                )
                            row_children.append(
                                dmc.TableTd(
                                    day_children,
                                    bg=MONTH_COLORS[
                                        datetime.datetime.fromisocalendar(
                                            iso_year, week, weekday
                                        ).month
                                    ],
                                )
                            )
                    row_children.append(dmc.TableTd(f"Calendar Week {week}"))
                    body_children.append(dmc.TableTr(row_children))

        # Create table body
        body = dmc.TableTbody(body_children)

        return [head, body]
