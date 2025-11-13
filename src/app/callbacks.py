"""
This module contains the callbacks of the application.
"""

from dash import Input, Output, clientside_callback


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
    )
