import pandas as pd
# research OSM
import geopandas as gpd
import shapely
import folium
import matplotlib.pyplot as plt
import osmnx as ox
import networkx as nx
import numpy as np
import os

from landprices import load_data_city


def get_total_length_for_each_nbh(city_name, neighborhood_path, network_types):
    """
    wrapper to get count data frame and automatically load data
    """

    city = gpd.read_file(f'{neighborhood_path}/Neighborhoods_{city_name}.gpkg')
    city = city.to_crs(epsg = 4326) # get geometry encoding right

    return get_path_length_per_nbh(city, network_types)


def get_path_length_per_nbh(city, network_types):
    """
    get a data frame for the edge length with the neighborhood names as columns and network type as rows
    """
    neighboorhood_names = city.Neighborhood_Name.values
    return_df =  pd.DataFrame(data=np.nan, index=network_types, columns=neighboorhood_names) # create empty df

    for nbh_name in neighboorhood_names:

        for network_type in network_types:
    
            # insert edge length for each neighborhood and network type
            return_df.loc[network_type, nbh_name] = get_edge_length_for_type(city, nbh_name, network_type)

        print(f'{nbh_name} done')

    return return_df

def get_edge_length_for_type(city, nbh_name, network_type):
    """
    get edge_length for a specific network_type and neighborhood
    """
    neighborhood = city.loc[city.Neighborhood_Name == nbh_name]
    try:
        G = ox.graph_from_polygon(neighborhood.geometry.iloc[0], network_type = network_type, simplify = True)
        edges = ox.graph_to_gdfs(G, nodes=False, edges=True)
        return edges['length'].sum()
    except ValueError as e:
        print(e)
        return 0



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
    # return a data frame with neighborhood as cols and amenity as row
    network_types = ['drive', 'bike', 'walk', 'drive_service', 'all', 'all_private']
    city = "Bremen"
    import time
    st = time.time()
    osm_result = get_total_length_for_each_nbh(city, "res/data/DLR/3 Neighborhoods", network_types).T
    osm_result = osm_result.reset_index(drop=False).rename(
        columns={"index": "Neighborhood_Name"}
    )
    city_distances = merge_osm_raster(
        gdf_osm=osm_result, gdf_city=load_data_city(city)
    )
    et = time.time()
    print('DURATION FOR LOADING: ', et-st)

    

    