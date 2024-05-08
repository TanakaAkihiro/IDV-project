import geopandas as gpd
from shapely.geometry import Point


def create_gdf(df):
    geometry = [Point(lon, lat) for lon, lat in zip(df["LONG"], df["LAT"])]
    df["geometry"] = geometry
    gdf = gpd.GeoDataFrame(df)
    return gdf


def preprocess_data(df, genus):
    gdf = create_gdf(df)
    lat = "LAT" if "LAT" in gdf.columns else "LATSTR"
    long = "LONG" if "LONG" in gdf.columns else "LONGSTR"
    site_name = "SITE_NAME" if "SITE_NAME" in gdf.columns else "NAME"
    gdff = gdf[
        [site_name, genus, lat, long, "geometry", "COUNTRY", "MIN_AGE", "MAX_AGE"]
    ]

    return gdff
