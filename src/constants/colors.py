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
}


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
