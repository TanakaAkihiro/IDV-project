import pandas as pd
from dash import callback, Output, Input
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.graph_objects as go
from utils.map import add_convex_hull_to_figure
from utils.dataframe import preprocess_data

df = pd.read_csv("data/ALLEurasia_modified.csv")
pred_df = pd.read_csv("data/ALLEurasia_MF.csv")


def register_callbacks():
    @callback(
        Output("main-map", "figure"),
        Input("genus-dropdown", "value"),
        Input("threshold-slider", "value"),
        Input("show-tru-occ-radio", "value"),
        Input("age-spans-dropdown", "value"),
    )
    def update_map(genus, threshold, show_occ, age_spans):
        if genus is None:
            raise PreventUpdate
        cols = [genus, "LAT", "LONG", "SITE_NAME", "COUNTRY", "MIN_AGE", "MAX_AGE"]

        pred_dff = pred_df[cols]
        pred_dff = pred_dff[df[genus] < 0.7]
        pred_dff = pred_dff[pred_dff[genus] >= threshold]

        dff = df[cols]
        dff = dff[dff[genus] >= 0.7]

        pred_gdff = preprocess_data(pred_dff, genus)

        fig = go.Figure()
        fig.add_trace(
            px.scatter_mapbox(
                pred_gdff,
                lon=pred_gdff.geometry.x,
                lat=pred_gdff.geometry.y,
                hover_data=["COUNTRY", "MIN_AGE", "MAX_AGE", genus],
                hover_name="SITE_NAME",
                color=genus,
            )
            .update_traces(mode="markers", marker=dict(size=7, opacity=0.7))
            .data[0]
        )

        if show_occ == "Yes":
            fig.add_trace(
                px.scatter_mapbox(
                    dff,
                    lon="LONG",
                    lat="LAT",
                    hover_data=["COUNTRY", "MIN_AGE", "MAX_AGE", genus],
                    hover_name="SITE_NAME",
                )
                .update_traces(
                    mode="markers", marker=dict(size=7, color="black", opacity=0.7)
                )
                .data[0]
            )

            if age_spans != [None] and age_spans != None:
                add_convex_hull_to_figure(
                    fig, dff=preprocess_data(dff, genus), age_spans=age_spans
                )

        fig.update_layout(
            margin=dict(l=0, r=0, b=0, t=0),
            autosize=True,
            height=800,
            mapbox_style="open-street-map",
            mapbox_center={
                "lat": pred_gdff.geometry.y.mean(),
                "lon": pred_gdff.geometry.x.mean(),
            },
            mapbox_zoom=1.7,
        )

        # fig.update_geos(projection_scale=1.5)

        return fig
