"""
This module contains the callbacks of the application.
"""

import datetime
import os

from dash import Input, Output, State, callback, clientside_callback
from dash.exceptions import PreventUpdate

from pages.activities.navbar import ActivitiesNavbar
from pages.activity.navbar import ActivityNavbar
from pages.home.navbar import HomeNavbar
from pages.map.navbar import MapNavbar
from strava.client import CLIENT

BASE_PATHNAME = os.getenv("BASE_PATHNAME")


def register_callbacks():
    """
    Register callbacks of the application.
    """

    clientside_callback(
        """
        (switchOn) => {
            document.documentElement.setAttribute(
                'data-mantine-color-scheme', switchOn ? 'dark' : 'light'
            );
            return window.dash_clientside.no_update
        }
        """,
        Output("color-scheme-switch", "id"),
        Input("color-scheme-switch", "checked"),
    )  # Set the color scheme of the application based on the switch state

    @callback(
        Output("activities-store", "data"),
        Input("app-start-interval", "n_intervals"),
        State("activities-store", "data"),
    )
    def load_activities(_, data):
        """
        Update the activities table with data from Strava client.
        """
        if data is not None and data != {}:
            raise PreventUpdate

        print("Loading activities data...")
        start_date = datetime.datetime.now() - datetime.timedelta(weeks=10)
        activities = CLIENT.get_activities(after=start_date)
        data = []
        for activity in activities:
            data.append(activity.model_dump())
        data.reverse()
        return data

    @callback(
        Output("navbar", "children"),
        Input("url", "pathname"),
    )
    def set_navbar(pathname):
        """
        Set the navbar content based on the current page.
        """
        if pathname is None:
            raise PreventUpdate

        if pathname == f"{BASE_PATHNAME}":
            return HomeNavbar()
        if pathname == f"{BASE_PATHNAME}activities":
            return ActivitiesNavbar()
        if pathname.startswith(f"{BASE_PATHNAME}activity/"):
            return ActivityNavbar()
        if pathname == f"{BASE_PATHNAME}map":
            return MapNavbar()
        return []
