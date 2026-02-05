"""
This module contains the color constants.
"""

import branca.colormap as cm

# Cycling
GRAVELBIKERIDE = "#fc6f03"
MOUTAINBIKERIDE = "#fc9d03"
RIDE = "#FF0000"
# Running
RUN = "#00FF00"
TRAILRUN = "#086808"
# Walk
HIKE = "#fc037f"
WALK = "#fc03f8"
SNOWSHOE = "#03fcf4"
# Other
SWIM = "#0000FF"
DEFAULT = "#FFFFFF"

SPORT_TYPE_COLORS = {
    # Cycling
    "GravelBikeRide": GRAVELBIKERIDE,
    "MountainBikeRide": MOUTAINBIKERIDE,
    "Ride": RIDE,
    # Running
    "Run": RUN,
    "TrailRun": TRAILRUN,
    # Walking
    "Hike": HIKE,
    "Walk": WALK,
    "Snowshoe": SNOWSHOE,
    # Other
    "Swim": SWIM,
}  # TODO add support for more sports
# https://support.strava.com/hc/en-us/articles/216919407-Supported-Sport-Types-on-Strava


# Colormaps
COLORMAPS = {
    "distance": cm.LinearColormap(["gold", "black"]),
    "altitude": cm.LinearColormap(["midnightblue", "skyblue"]),
    "velocity_smooth": cm.LinearColormap(["teal", "cyan"]),
    "heartrate": cm.LinearColormap(["lightcoral", "red"]),
    "cadence": cm.LinearColormap(["pink", "purple"]),
    "watts": cm.LinearColormap(["moccasin", "darkorange"]),
    "grade_smooth": cm.LinearColormap(["crimson", "black"]),
}

DIFFICULTY_COLORMAP = cm.LinearColormap(["green", "yellow", "orange", "red"])

# Months
MONTH_COLORS = {
    1: "#D6E6F2",  # January
    2: "#C9DDF0",  # February
    3: "#CFE8E4",  # March
    4: "#DFF1D6",  # April
    5: "#F1F7C4",  # May
    6: "#FFF1C1",  # June
    7: "#FFD6C9",  # July
    8: "#FFB7B2",  # August
    9: "#FFD8A8",  # September
    10: "#F4C2C2",  # October
    11: "#E6CFE6",  # November
    12: "#D8DFF0",  # December
}
