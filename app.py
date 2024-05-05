import pandas as pd
import geopandas as gpd
import dash
from dash import html, dcc, Input, Output, callback
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.graph_objects as go
from shapely.geometry import Point


df = pd.read_csv("data/ALLEurasia_modified.csv")
gdf = gpd.GeoDataFrame(
    df, geometry=[Point(lon, lat) for lon, lat in zip(df["LONG"], df["LAT"])]
)

pred_df = pd.read_csv("data/ALLEurasia_MF.csv")
pred_gdf = gpd.GeoDataFrame(
    pred_df, geometry=[Point(lon, lat) for lon, lat in zip(pred_df["LONG"], pred_df["LAT"])]
)


app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([
    html.Div([
        html.Label("Genus"),
        dcc.Dropdown(id="genus-dropdown", options=df.columns)
    ]),
    dcc.Graph(id="main-map"),
    dcc.Slider(0, 1, 0.1, value=0, id="threshold-slider")
])

@callback(
    Output("main-map", "figure"),
    Input("genus-dropdown", "value"),
    Input("threshold-slider", "value")
)
def update_map(genus, threshold):
    if genus is None:
        raise PreventUpdate
    cols = [genus, "LAT", "LONG", "SITE_NAME", "COUNTRY", "MIN_AGE", "MAX_AGE"]
    dff = df[cols]
    dff = dff[dff[genus] >= threshold]
    pred_dff = pred_df[cols]
    pred_dff = pred_dff[pred_dff[genus] >= threshold]


    fig = go.Figure()
    fig.add_trace(
        px.scatter_geo(
            pred_dff,
            lon='LONG',
            lat='LAT',
            hover_data=["COUNTRY", "MIN_AGE", "MAX_AGE", genus],
            hover_name="SITE_NAME",
            color=genus
        )
        .update_traces(marker={"symbol": "circle"})
        .data[0]
    )
    
    fig.add_trace(
        px.scatter_geo(
            dff,
            lon='LONG',
            lat='LAT',
            hover_data=["COUNTRY", "MIN_AGE", "MAX_AGE"],
            hover_name="SITE_NAME"
        ).update_traces(marker=dict(symbol="cross", color="black")).data[0]
    )

    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0),
                  width=1800,
                  height=800)
    
    return fig

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port="8050")