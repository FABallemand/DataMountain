"""
This module contains the layout of the Activity page.
"""

import dash
import dash_mantine_components as dmc

from .callbacks import register_callbacks
from .tabs.overview.layout import OverviewLayout
from .tabs.statistics.layout import StatisticsLayout

dash.register_page(
    __name__, name="Activity", path_template="/activity/<activity_id>", order=None
)

register_callbacks()


def layout(activity_id):  # pylint: disable=unused-argument
    """
    Define the layout of the Activity page.
    """
    return dmc.Container(
        [
            dmc.Title(
                id={
                    "page": "activity",
                    "component": "title",
                },
                order=1,
            ),
            dmc.Tabs(
                [
                    dmc.TabsList(
                        [
                            dmc.TabsTab("Overview", value="overview"),
                            dmc.TabsTab("Statistics", value="statistics"),
                        ]
                    ),
                    dmc.TabsPanel(OverviewLayout(), value="overview"),
                    dmc.TabsPanel(StatisticsLayout(), value="statistics"),
                ],
                value="overview",
                variant="outline",
            ),
        ],
        fluid=True,
    )
