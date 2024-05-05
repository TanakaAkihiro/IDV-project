import pandas as pd
from dash import callback, Output, Input
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv("data/ALLEurasia_modified.csv")
pred_df = pd.read_csv("data/ALLEurasia_MF.csv")


def register_callbacks():
    @callback(
        Output("main-map", "figure"),
        Input("genus-dropdown", "value"),
        Input("threshold-slider", "value"),
        Input("show-tru-occ-radio", "value"),
    )
    def update_map(genus, threshold, show_occ):
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
            .update_traces(marker=dict(size=7, symbol="circle", opacity=0.7))
            .data[0]
        )

        if show_occ == "Yes":
            fig.add_trace(
                px.scatter_geo(
                    dff,
                    lon="LONG",
                    lat="LAT",
                    hover_data=["COUNTRY", "MIN_AGE", "MAX_AGE", genus],
                    hover_name="SITE_NAME",
                )
                .update_traces(
                    marker=dict(size=7, symbol="cross", color="black", opacity=0.7)
                )
                .data[0]
            )

        fig.update_layout(
            margin=dict(l=0, r=0, b=0, t=0),
            autosize=True,
            height=800,
            geo={"center": {"lat": df["LAT"].mean(), "lon": df["LONG"].mean()}},
        )

        fig.update_geos(projection_scale=1.5)

        return fig
