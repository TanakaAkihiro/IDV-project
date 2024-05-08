import geopandas as gpd
from shapely.geometry import Point
import plotly.express as px


COLORS = [
    "rgba(255, 0, 0, 0.3)",
    "rgba(0, 0, 255, 0.3)",
    "rgba(255, 255, 0, 0.3)",
    "rgba(0, 255, 0, 0.3)",
    "rgba(0, 255, 255, 0.3)",
    "rgba(255, 0, 255, 0.3)",
]


def get_initial_map():
    fig = px.scatter_mapbox({}, [], [])
    fig.update_layout(
        margin=dict(l=0, r=0, b=0, t=0),
        autosize=True,
        height=800,
        mapbox_style="open-street-map",
        mapbox_zoom=1.7,
    )
    return fig


def add_convex_hull_to_figure(fig, dff, age_spans):
    geometry = [Point(lon, lat) for lon, lat in zip(dff["LONG"], dff["LAT"])]
    dff["geometry"] = geometry
    gdff = gpd.GeoDataFrame(dff)

    gdffs = {}

    if isinstance(age_spans, str):
        age_spans = [age_spans]

    for a in age_spans:
        start, end = a.split("-")
        gdffs[a] = gdff[
            (gdff["MIN_AGE"] >= float(start)) & (gdff["MAX_AGE"] < float(end))
        ]

    errors = []

    for i, (age_span, gdf) in enumerate(gdffs.items()):
        # Skip drawing a convex hull if it has less than three points
        if len(gdf.drop_duplicates(subset=["LAT", "LONG"])) < 3:
            errors.append(age_span)
            continue

        convex_hull = gdf.unary_union.convex_hull

        fig.add_scattermapbox(
            lat=list(convex_hull.exterior.xy[1]),
            lon=list(convex_hull.exterior.xy[0]),
            fill="toself",
            fillcolor=COLORS[i],
            mode="lines",
            line=dict(color=COLORS[i], width=2),
            name=age_span,
        )

    fig.update_layout(legend=dict(x=1.025, y=0.5, yanchor="top"))

    return errors
