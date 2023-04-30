import sys
import os

import pandas as pd

os.environ["USE_PYGEOS"] = "0"
import geopandas as gpd

from helper.landprice_merger import (
    zensus_landprice_merger,
    landprice_neighborhood_merger,
    combine_landprice_with_geodata,
)
from helper.csv_merger import combine_csvs
from helper.principal_component_analysis import combine_PCA_datasets


def load_data_city(str_city: str) -> gpd.GeoDataFrame:
    main_path = os.getcwd()

    path_zensus = os.path.join(main_path, "res", "data", "DLR", "2 Zensus")
    path_land = os.path.join(main_path, "res", "data", "DLR", "1 Land Prices")
    path_neigh = os.path.join(main_path, "res", "data", "DLR", "3 Neighborhoods")

    df_zensus = combine_csvs(str_path=path_zensus)

    gdf_zensus, important_features_city_source = combine_PCA_datasets(
        df_zensus=df_zensus, str_city=str_city, str_path=path_zensus
    )

    df_land_prices = combine_csvs(str_path=path_land)

    gdf_landprices = combine_landprice_with_geodata(
        df_landprice=df_land_prices, str_city=str_city, str_path=path_land
    )

    gdf_landprices_names = landprice_neighborhood_merger(
        gdf_landprice=gdf_landprices, str_city=str_city, str_path_neigh=path_neigh
    )

    return zensus_landprice_merger(
        gdf_landprices=gdf_landprices_names, gdf_zensus=gdf_zensus
    )


if __name__ == "__main__":
    cities = ["Berlin", "Bremen", "Dresden", "Frankfurt_am_Main", "Köln"]
    result = load_data_city(cities[0])
