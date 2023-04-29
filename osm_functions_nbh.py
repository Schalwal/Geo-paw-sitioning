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

def get_count_nbh(city_name, neighborhood_path, amenities_lst=['restaurant', 'cafe', 'school']):
    """
    return df with occurence for each amenity in each neighborhood and read in file
    """
    city = gpd.read_file(f'{neighborhood_path}/Neighborhoods_{city_name}.gpkg')
    city = city.to_crs(epsg = 4326) # get geometry encoding right

    return get_df_count_per_nbh(city, amenities_lst)


def get_df_count_per_nbh(city, amenities_lst):
    """
    Get get count for different amenities in a per Neighborhood
    """

    # loop over different neighborhoods
    neighboorhood_names = city.Neighborhood_Name.values
    return_df =  pd.DataFrame(data=np.nan, index=amenities_lst, columns=neighboorhood_names)

    # for each neighborhood
    for nbh_name in neighboorhood_names:
        
        temp_df = get_geometry_df_with_amenity_tag(city, nbh_name, amenities_lst)
        
        # for each amenity..
        for amenity in amenities_lst:
    
            # .. insert count of occurences
            return_df.loc[amenity, nbh_name] = int(temp_df[temp_df.amenity==amenity].shape[0]) if 'amenity' in temp_df.columns else 0

        # print(f'{nbh_name} done')

    return return_df


def get_geometry_df_with_amenity_tag(city, nbh_name, amenities_lst):
    """
    get df with information on each amenity uni in the given neighborhood
    """

    # exctract neighborhood from city
    neighborhood = city.loc[city.Neighborhood_Name == nbh_name]

    # define df with all elements of each amenity
    amenity_df = ox.geometries.geometries_from_polygon(
            polygon = neighborhood.geometry.iloc[0],
            tags = {"amenity":amenities_lst}
            )
    return amenity_df