import osm_distance_total
import osm_functions_nbh
import landprices

def osm_wrapper():

    from time import time

    amenities_lst=["restaurant", "cafe", "school", "administration", "advertising",
                   "archive", "bench", "ev charging", "financial advice", "gym", "hotel", "park",
                   "library", "refugee housing", "student accommodation", "nursery", "preschool",
                   "public building", "shop", "sport school", "hospital"]
    network_types = ['drive', 'bike', 'walk', 'drive_service', 'all', 'all_private']
    city = "Bremen"
 
    st = time()

    # 1. Distance
    osm_result_distance = osm_distance_total.get_total_length_for_each_nbh(city, "res/data/DLR/3 Neighborhoods", network_types).T
    osm_result_distance = osm_result_distance.reset_index(drop=False).rename(
        columns={"index": "Neighborhood_Name"}
    )
    city_distances = osm_distance_total.merge_osm_raster(
        gdf_osm=osm_result_distance, gdf_city=landprices.load_data_city(city)
    )

    mt = time()
    print('HALF TIME: ', (mt-st)/60, 'minutes until now.')

    # 2. Count onto Distance df
    osm_result_count = osm_functions_nbh.get_count_nbh(city, "res/data/DLR/3 Neighborhoods", amenities_lst).T
    osm_result_count = osm_result_count.reset_index(drop=False).rename(
        columns={"index": "Neighborhood_Name"}
    )

    # FINAL DATAFRAME
    merged_df = osm_functions_nbh.merge_osm_raster(
        gdf_osm=osm_result_count, gdf_city=city_distances
    )
    et = time()
    print('DONE! after ', (et-st)/60, 'minutes until now.')

    return merged_df





if __name__ == "__main__":

    from time import time

    amenities_lst=["restaurant", "cafe", "school", "administration", "advertising",
                   "archive", "bench", "ev charging", "financial advice", "gym", "hotel", "park",
                   "library", "refugee housing", "student accommodation", "nursery", "preschool",
                   "public building", "shop", "sport school", "hospital"]
    network_types = ['drive', 'bike', 'walk', 'drive_service', 'all', 'all_private']
    city = "Berlin"
 
    st = time()

    # 1. Distance
    osm_result_distance = osm_distance_total.get_total_length_for_each_nbh(city, "res/data/DLR/3 Neighborhoods", network_types).T
    osm_result_distance = osm_result_distance.reset_index(drop=False).rename(
        columns={"index": "Neighborhood_Name"}
    )
    city_distances = osm_distance_total.merge_osm_raster(
        gdf_osm=osm_result_distance, gdf_city=landprices.load_data_city(city)
    )

    mt = time()
    print('HALF TIME: ', (mt-st)/60, 'minutes until now.')

    # 2. Count onto Distance df
    osm_result_count = osm_functions_nbh.get_count_nbh(city, "res/data/DLR/3 Neighborhoods", amenities_lst).T
    osm_result_count = osm_result_count.reset_index(drop=False).rename(
        columns={"index": "Neighborhood_Name"}
    )

    # FINAL DATAFRAME
    merged_df = osm_functions_nbh.merge_osm_raster(
        gdf_osm=osm_result_count, gdf_city=city_distances
    )
    et = time()
    print('DONE! after ', (et-st)/60, 'minutes until now.')

    merged_df.to_csv(f'res/{city}_real.csv')

