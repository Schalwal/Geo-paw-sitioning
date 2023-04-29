import pandas as pd

# research OSM
import os

os.environ["USE_PYGEOS"] = "0"
import geopandas as gpd
import shapely
import folium
import matplotlib.pyplot as plt
import osmnx as ox
import networkx as nx
import numpy as np

from landprices import load_data_city


def get_count_nbh(
    city_name,
    neighborhood_path,
    amenities_lst=["restaurant", "cafe", "school", "administration", "advertising",
                   "archive", "bench", "ev charging", "financial advice", "gym", "hotel", "park",
                   "library", "refugee housing", "student accommodation", "nursery", "preschool",
                   "public building", "shop", "sport school", "hospital"]
):
    """
    return df with occurence for each amenity in each neighborhood and read in file
    """
    city = gpd.read_file(f"{neighborhood_path}/Neighborhoods_{city_name}.gpkg")
    city = city.to_crs(epsg=4326)  # get geometry encoding right

    return get_df_count_per_nbh(city, amenities_lst)


def get_df_count_per_nbh(city, amenities_lst):
    """
    Get get count for different amenities in a per Neighborhood
    """

    # loop over different neighborhoods
    neighboorhood_names = city.Neighborhood_Name.values
    return_df = pd.DataFrame(
        data=np.nan, index=amenities_lst, columns=neighboorhood_names
    )

    # for each neighborhood
    for nbh_name in neighboorhood_names:
        temp_df = get_geometry_df_with_amenity_tag(city, nbh_name, amenities_lst)

        # for each amenity..
        for amenity in amenities_lst:
            # .. insert count of occurences
            return_df.loc[amenity, nbh_name] = (
                int(temp_df[temp_df.amenity == amenity].shape[0])
                if "amenity" in temp_df.columns
                else 0
            )

        # print(f'{nbh_name} done')

    return return_df


def get_geometry_df_with_amenity_tag(city, nbh_name, amenities_lst):
    """
    get df with information on each amenity unit in the given neighborhood
    """

    # exctract neighborhood from city
    neighborhood = city.loc[city.Neighborhood_Name == nbh_name]

    # define df with all elements of each amenity
    amenity_df = ox.geometries.geometries_from_polygon(
        polygon=neighborhood.geometry.iloc[0], tags={"amenity": amenities_lst}
    )
    return amenity_df


def merge_osm_raster(
    gdf_osm: pd.DataFrame, gdf_city: gpd.GeoDataFrame
) -> gpd.GeoDataFrame:
    """
    merging osm ammenity data with city-raster GeoDataFrame
    """
    return gpd.GeoDataFrame(
        pd.merge(left=gdf_city, right=gdf_osm, how="left", on="Neighborhood_Name")
    )


if __name__ == "__main__":
    city = "Berlin"
    osm_result = get_count_nbh(city, "res/data/DLR/3 Neighborhoods").T
    osm_result = osm_result.reset_index(drop=False).rename(
        columns={"index": "Neighborhood_Name"}
    )
    city_ammenities = merge_osm_raster(
        gdf_osm=osm_result, gdf_city=load_data_city(city)
    )
