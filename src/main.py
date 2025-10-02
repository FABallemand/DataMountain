# pylint: disable=ungrouped-imports
"""
Main file to launch the Dash webapp.
"""

import os
import sys

import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import dcc, html
from dotenv import load_dotenv

#######################################################################
## Environment Setup ##################################################
#######################################################################

load_dotenv(override=True)  # Load environment variables from .env

#######################################################################
## Dash Setup #########################################################
#######################################################################


## Layout #############################################################
def serve_layout():
    """
    Define the layout of the application.
    """
    return dmc.MantineProvider(
        html.Div(
            [
                dcc.Location(id="url"),
                dcc.Interval(
                    id="startup_interval", interval=10, n_intervals=0, max_intervals=1
                ),  # Trigger once 10ms fater app start
                # Products data stores
                dcc.Store(id="products_data_store", data={}),
                dcc.Store(id="products_profiles_store", storage_type="local", data={}),
                # Stabi data stores
                dcc.Store(id="stabi_data_store", data={}),
                dcc.Store(id="stabi_profiles_store", storage_type="local", data={}),
                # Time series data stores
                dcc.Store(id="ts_data_store", data={}),
                # Navbar(),
                dash.page_container,
            ],
            style={
                "display": "flex",
                "flexDirection": "column",  # Stack children vertically
                "overflow": "hidden",  # Prevent overall page scrolling
            },
        )
    )


## App ################################################################
app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    title="DataVista",
    url_base_pathname=os.getenv("BASE_PATHNAME"),
)

app.layout = serve_layout  # Set the layout of the application

#######################################################################
## Launch App #########################################################
#######################################################################

if __name__ == "__main__":
    print("==== RUN APP ====")
    if len(sys.argv) > 1:
        if sys.argv[1] == "nginx":
            from waitress import serve
            from werkzeug.middleware.proxy_fix import ProxyFix

            app.server.wsgi_app = ProxyFix(
                app.server.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
            )
            serve(app.server, host=os.getenv("IP_ADDRESS"), port=os.getenv("PORT"))
        elif sys.argv[1] == "waitress":
            from waitress import serve

            serve(app.server, host=os.getenv("IP_ADDRESS"), port=os.getenv("PORT"))
        elif sys.argv[1] == "local":
            app.run(debug=False)
        elif sys.argv[1] == "debug":
            app.run(debug=True)
        elif sys.argv[1] == "profile":
            from werkzeug.middleware.profiler import ProfilerMiddleware

            app.server.wsgi_app = ProfilerMiddleware(
                app.server.wsgi_app, sort_by=("cumtime", "tottime"), restrictions=[50]
            )
            app.run(debug=False)
        else:
            print(f"Invalid argument {sys.argv[1]}, default with: app.run(debug=True)")
            app.run(debug=True)
    else:
        print("No argument specified, default with: app.run(debug=True)")
        app.run(debug=True)
