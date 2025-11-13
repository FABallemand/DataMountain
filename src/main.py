# pylint: disable=ungrouped-imports
"""
Main file to launch the Dash webapp.
"""

import os
import sys

import dash
from dotenv import load_dotenv

from app.callbacks import register_callbacks
from app.layout import Layout

#######################################################################
## Environment Setup ##################################################
#######################################################################

load_dotenv(override=True)  # Load environment variables from .env

#######################################################################
## Dash Setup #########################################################
#######################################################################

app = dash.Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    title="Data Moutain",
    url_base_pathname=os.getenv("BASE_PATHNAME"),
)
app.layout = Layout  # Set the layout of the application
register_callbacks()  # Register application callbacks

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
