import os
import pandas as pd

os.environ["USE_PYGEOS"] = "0"
import geopandas as gpd

from csv_merger import combine_csvs
from principal_component_analysis import combine_PCA_datasets


def combine_landprice_with_geodata(
    df_landprice: pd.DataFrame, str_city: str, str_path: str
) -> gpd.GeoDataFrame:
    """
    Returns geodataframe for landprices on grid-level

            Parameters:
                    df_landprice (pd.DataFrame): DataFrame for landprice data
                    str_city (str): String of city name
                    str_path (str): String to directory of source

            Returns:
                    price_grid (gpd.GeoDataFrame): GeoDataFrame for landprice by city
    """

    ls_files_gpkg = [
        file
        for file in os.listdir(str_path)
        if file.endswith(".gpkg") and str_city in file
    ]

    price_grid = gpd.read_file(os.path.join(str_path, ls_files_gpkg[0]))

    df_land_prices_city = df_landprice[
        df_landprice["City_Name"] == str_city
    ].reset_index(drop=True)

    price_grid = price_grid.merge(
        df_land_prices_city,
        on=["Neighborhood_FID", "Land_Value", "Area_Count", "City_Name"],
        how="inner",
    )

    return price_grid


def landprice_neighborhood_merger(
    gdf_landprice: gpd.GeoDataFrame, str_city: str, str_path_neigh: str
) -> gpd.GeoDataFrame:
    """
    Returns GeoDataFrame for landprices with Neighborhood_Name and District_Name

            Parameters:
                    gdf_landprice (gpd.GeoDataFrame): GeoDataFrame for landprice data
                    str_city (str): String of city name
                    str_path_neigh (str): String to directory of source

            Returns:
                    (gpd.GeoDataFrame): GeoDataFrame for landprice by city with Neighborhood_Name and District_Name
    """
    ls_gpkg = [
        file
        for file in os.listdir(str_path_neigh)
        if file.endswith(".gpkg") and str_city in file
    ]
    gdf_neighborhoods = gpd.read_file(os.path.join(str_path_neigh, ls_gpkg[0]))
    return gpd.GeoDataFrame(
        pd.merge(
            left=gdf_landprice,
            right=gdf_neighborhoods[
                ["Neighborhood_FID", "Neighborhood_Name", "District_Name"]
            ],
        )
    )


def zensus_landprice_merger(
    gdf_landprices: gpd.GeoDataFrame, gdf_zensus: gpd.GeoDataFrame
) -> gpd.GeoDataFrame:
    """
    Returns gdf_lanprices and gdf_zensus merge

            Parameters:
                    gdf_landprice (gpd.GeoDataFrame): GeoDataFrame for landprice data
                    gdf_zensus (gpd.GeoDataFrame): GeoDataFrame for zensus data

            Returns:
                    (gpd.GeoDataFrame): GeoDataFrame of gdf_lanprices and gdf_zensus merge on raster-level
    """
    return gpd.sjoin(left_df=gdf_zensus, right_df=gdf_landprices, how="left")


if __name__ == "__main__":
    main_path = os.getcwd()

    path_land = os.path.join(main_path, "res", "data", "DLR", "1 Land Prices")
    df_land_prices = combine_csvs(str_path=path_land)

    cities = ["Berlin", "Bremen", "Dresden", "Frankfurt", "Köln"]
    """for city in cities:
        df_landprices = combine_landprice_with_geodata(df_land_prices, city, path_land)"""
    gdf_landprices = combine_landprice_with_geodata(
        df_landprice=df_land_prices, str_city=cities[0], str_path=path_land
    )

    path_neigh = os.path.join(main_path, "res", "data", "DLR", "3 Neighborhoods")
    gdf_landprices_names = landprice_neighborhood_merger(
        gdf_landprice=gdf_landprices, str_city=cities[0], str_path_neigh=path_neigh
    )

    path_zensus = os.path.join(main_path, "res", "data", "DLR", "2 Zensus")
    df_zensus = combine_csvs(str_path=path_zensus)
    gdf_zensus = combine_PCA_datasets(
        df_zensus=df_zensus, str_city=cities[0], str_path=path_zensus
    )

    gdf_raster = zensus_landprice_merger(
        gdf_landprices=gdf_landprices_names, gdf_zensus=gdf_zensus
    )
