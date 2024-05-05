import pandas as pd
from dash import html, dcc
from utils.map import get_initial_map


df = pd.read_csv("data/ALLEurasia_modified.csv")


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
                    )
                    
                ],
                id="controls",
                className="controls",
            ),
        ],
        id="container",
        className="container",
    )