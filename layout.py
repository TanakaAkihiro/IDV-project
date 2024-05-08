import pandas as pd
from dash import html, dcc
from utils.map import get_initial_map


df = pd.read_csv("data/ALLEurasia_modified.csv")

AGE_SPANS = ["0-0.1", "0.1-0.6", "0.6-1.1", "1.1-1.6", "1.6-2.1", "2.1-2.6"]

def get_layout():
    return html.Div(
        [
            dcc.Graph(id="main-map", figure=get_initial_map()),
            html.Div(
                [
                    html.Div(
                        [
                            html.Label("Genus"),
                            dcc.Dropdown(id="genus-dropdown", options=df.columns),
                        ],
                        className="genus-dropdown",
                    ),
                    html.Div(
                        [
                            html.Label("Threshold"),
                            dcc.Slider(0, 1, 0.1, value=0, id="threshold-slider"),
                        ],
                        className="threshold-slider",
                    ),
                    html.Div(
                        [
                            html.Label("Show true occurrences"),
                            dcc.RadioItems(
                                ["Yes", "No"],
                                "Yes",
                                id="show-tru-occ-radio",
                                inline=True,
                            ),
                        ],
                        className="show-tru-occ-radio",
                    ),
                    html.Div(
                        [
                            html.Label("Age spans"),
                            dcc.Dropdown(
                                AGE_SPANS,
                                id="age-spans-dropdown",
                                multi=True
                            )
                        ],
                        className="age-spans-dropdown",
                    )
                ],
                id="controls",
                className="controls",
            ),
        ],
        id="container",
        className="container",
    )
