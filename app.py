import pandas as pd
import dash
from dash import html, dcc, Input, Output, callback
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.graph_objects as go
from utils.map import get_initial_map


df = pd.read_csv("data/ALLEurasia_modified.csv")

pred_df = pd.read_csv("data/ALLEurasia_MF.csv")


app = dash.Dash(__name__)

server = app.server

app.layout = html.Div(
    [
        dcc.Graph(id="main-map", figure=get_initial_map()),
        html.Div(
            [
                html.Div(
                    [
                        html.Label("Genus"),
                        dcc.Dropdown(id="genus-dropdown", options=df.columns),
                    ]
                ),
                dcc.Slider(0, 1, 0.1, value=0, id="threshold-slider"),
            ],
            id="controls",
            className="controls",
        ),
    ],
    id="container",
    className="container",
)


@callback(
    Output("main-map", "figure"),
    Input("genus-dropdown", "value"),
    Input("threshold-slider", "value"),
)
def update_map(genus, threshold):
    if genus is None:
        raise PreventUpdate
    cols = [genus, "LAT", "LONG", "SITE_NAME", "COUNTRY", "MIN_AGE", "MAX_AGE"]

    pred_dff = pred_df[cols]
    pred_dff = pred_dff[df[genus] < 0.7]
    pred_dff = pred_dff[pred_dff[genus] >= threshold]

    dff = df[cols]
    dff = dff[dff[genus] >= 0.7]

    fig = go.Figure()
    fig.add_trace(
        px.scatter_geo(
            pred_dff,
            lon="LONG",
            lat="LAT",
            hover_data=["COUNTRY", "MIN_AGE", "MAX_AGE", genus],
            hover_name="SITE_NAME",
            color=genus,
        )
        .update_traces(marker={"symbol": "circle"})
        .data[0]
    )

    fig.add_trace(
        px.scatter_geo(
            dff,
            lon="LONG",
            lat="LAT",
            hover_data=["COUNTRY", "MIN_AGE", "MAX_AGE", genus],
            hover_name="SITE_NAME",
        )
        .update_traces(marker=dict(symbol="cross", color="black"))
        .data[0]
    )

    fig.update_layout(
        margin=dict(l=0, r=0, b=0, t=0),
        width=1800,
        height=800,
        geo={"center": {"lat": df["LAT"].mean(), "lon": df["LONG"].mean()}},
    )

    fig.update_geos(projection_scale=1.5)

    return fig


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port="8050")
