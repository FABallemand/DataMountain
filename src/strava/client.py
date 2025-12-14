"""
Client setup for Stravalib.
"""

import os

from stravalib import Client

access_token = os.getenv("STRAVA_ACCESS_TOKEN")
if not access_token:
    raise EnvironmentError("STRAVA_ACCESS_TOKEN environment variable is missing")

token_expires = os.getenv("STRAVA_TOKEN_EXPIRES")
if not token_expires:
    raise EnvironmentError("STRAVA_TOKEN_EXPIRES environment variable is missing")
token_expires = int(token_expires)

refresh_token = os.getenv("STRAVA_REFRESH_TOKEN")
if not refresh_token:
    raise EnvironmentError("STRAVA_REFRESH_TOKEN environment variable is missing")

CLIENT = Client(
    access_token=access_token,
    token_expires=token_expires,
    refresh_token=refresh_token,
)
