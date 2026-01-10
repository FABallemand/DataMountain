"""
This module contains the layout of the Activities page.
"""

import dash

# import dash_ag_grid as dag
import dash_mantine_components as dmc

from .callbacks import register_callbacks

dash.register_page(__name__, name="Activities", path="/activities", order=2)

register_callbacks()

layout = dmc.Container(
    dmc.Stack(
        [
            # dag.AgGrid(
            #     id={"page": "activities", "component": "activities-table"},
            #     columnDefs=[
            #         {"field": "id"},
            #         {"field": "name"},
            #         {"field": "sport_type"},
            #         {"field": "start_date_local"},
            #         {"field": "elapsed_time"},
            #         {"field": "distance"},
            #         {"field": "total_elevation_gain"},
            #         {"field": "average_heartrate"},
            #         {"field": "kudos_count"},
            #         {"field": "private"},
            #         {"field": "visibility"},
            #     ],
            # ),
            dmc.SimpleGrid(
                id={"page": "activities", "component": "activities-list"},
                cols=4,
                spacing="md",
                verticalSpacing="md",
            ),
        ],
    ),
    fluid=True,
)
