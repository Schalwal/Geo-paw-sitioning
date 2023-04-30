import os

os.environ["USE_PYGEOS"] = "0"

from shapely import wkt
import geopandas as gpd
import pandas as pd


def load_neighborhood(p: str) -> gpd.GeoDataFrame:
    return gpd.read_file(p)


def load_city(p: str) -> pd.DataFrame:
    return pd.read_csv(p, index_col=0)


def slice_df(df: pd.DataFrame) -> pd.DataFrame:
    return df[["Neighborhood_FID", "Neighborhood_Name"]]


def merge_gdfs(gdf_nbh: gpd.GeoDataFrame, df_city: pd.DataFrame) -> gpd.GeoDataFrame:
    return gpd.GeoDataFrame(
        gdf_nbh[["Neighborhood_FID", "Neighborhood_Name", "geometry"]].merge(
            df_city, on=["Neighborhood_FID", "Neighborhood_Name"]
        )
    )


def write_gdf(gdf: gpd.GeoDataFrame, p: str):
    gdf.to_csv(p)


if __name__ == "__main__":
    cities = {
        "Berlin": "Berlin",
        "Bremen": "Bremen",
        "Dresden": "Dresden",
        "Frankfurt": "Frankfurt_am_Main",
        "Koeln": "Köln",
    }
    for model, nbh in cities.items():
        p_nbh = f"res/data/DLR/3 Neighborhoods/Neighborhoods_{nbh}.gpkg"
        gdf_nbh = load_neighborhood(p=p_nbh)

        p_city = f"res/data/model_ouputs/{model}.csv"
        df_city = load_city(p=p_city)
        gdf_city = slice_df(df=df_city)
        gdf_merged = merge_gdfs(gdf_nbh=gdf_nbh, df_city=df_city)

        p_out = f"res/data/plotting/{model}_plotting.csv"
        write_gdf(gdf=gdf_merged, p=p_out)
