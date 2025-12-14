# pylint: disable=invalid-name
# Disable invalid name to match dash PascalCase
"""
This module contains the layout of the application.
"""

import os

import dash
import dash_mantine_components as dmc
from dash import dcc
from dash_iconify import DashIconify


def Pages():
    """
    Create the layout of the header's page selection.
    """
    return [
        dmc.Anchor(page["name"], href=os.getenv("BASE_PATHNAME") + page["path"][1:])
        for page in dash.page_registry.values()
    ]


def Header():
    """
    Create the layout of the header.
    """
    return dmc.AppShellHeader(
        dmc.Group(
            [
                dmc.Group(
                    [
                        dmc.Burger(
                            id="burger", size="sm", hiddenFrom="sm", opened=False
                        ),
                        # dmc.Image(src=logo, h=40, flex=0),
                        dmc.Title("Data Mountain"),
                        *Pages(),
                    ],
                ),
                dmc.Group(
                    [
                        dmc.Switch(
                            id="color-scheme-switch",
                            offLabel=DashIconify(icon="radix-icons:moon", width=20),
                            onLabel=DashIconify(icon="radix-icons:sun", width=20),
                            size="lg",
                        )
                    ],
                ),
            ],
            h="100%",
            justify="space-around",
        )
    )


def Navbar():
    """
    Create the layout of the navbar.
    """
    return dmc.AppShellNavbar(
        id="navbar",
        children=[],
        p="md",
    )


def Layout():
    """
    Create the layout of the application.
    """
    return dmc.MantineProvider(
        dmc.AppShell(
            [
                # Hidden components
                dcc.Location(id="url"),
                dcc.Store(id="athlete-store", data={}),
                dcc.Store(id="activities-store", data={}),
                dcc.Interval(
                    id="app-start-interval", interval=10, max_intervals=1
                ),  # Trigger once on app start
                # Visible components
                Header(),
                Navbar(),
                dmc.AppShellMain(dash.page_container),
            ],
            header={"height": 60},
            padding="md",
            navbar={
                "width": 300,
                "breakpoint": "sm",
                "collapsed": {"mobile": True},
            },
            id="appshell",
        )
    )
