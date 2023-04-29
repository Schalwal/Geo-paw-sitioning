import streamlit as st
import os
import glob
import numpy as np
import pandas as pd
import geopandas as gpd
import folium
#from combine_csv import combine_csv
from streamlit_folium import st_folium


# streamlit run st_app.py

def combine_csv(str_path):

    """
    Takes one argument: Full path of csv files
    """

    os.chdir(str_path)

    ls_files = glob.glob('*.{}'.format("csv"))
    ls_df = []

    if "Land Prices" in str_path:
            
        for file in ls_files:
            ls_df.append(pd.read_csv(file, delimiter = ";"))

        df_combined = pd.concat(ls_df).drop(columns = ["Unnamed: 0"]).reset_index(drop = True)
    
        ls_categorial_columns = list(df_combined["Area_Types"].str.split("_", expand = True).value_counts().index.values[0])

        for col in ls_categorial_columns:

            df_combined[col] = 0

        df_categories_raw = df_combined["Area_Types"].str.split("_", expand = True)

        for i in range(len(df_combined)):

            df_categories_raw_row = df_categories_raw.iloc[i].dropna()

            for column in ls_categorial_columns:

                if column in df_categories_raw_row.values:
                    df_combined[column].iloc[i] += 1

        return df_combined.drop(columns = ["Area_Types"])

    elif "Zensus" in str_path:

        for file in ls_files:
                
            df_temp = pd.read_csv(file, delimiter = ";")
            df_temp["City"] = file.split("_")[1].split(".")[0]
            df_temp["zensus_source"] = file.split("_")[-1].split(".")[0]
            ls_df.append(df_temp)

        return pd.concat(ls_df).drop(columns = ["Unnamed: 0"]).reset_index(drop = True)
    
    else:

        return "No appropriate folder to process"

def create_map(city):
    df = combine_csv("D:\\GitHub\\Geo-paw-sitioning\\1 Land Prices")
    df_city = df.loc[df["City_Name"] == city]
    df_city = df_city.drop(columns=['Land_Value', 'Area_Count', 'City_Name']) 
    gdf_city = gpd.read_file("D:\\GitHub\\Geo-paw-sitioning\\1 Land Prices\\Land_Prices_Neighborhood_" + city + ".gpkg")
    gdf_city = gdf_city.drop(columns = ['Area_Types'])
    gdf_city = gdf_city.merge(df_city, on='Neighborhood_FID')
    m = gdf_city.explore(height=500, width=1000, name="Neighborhoods")
    m = gdf_city.explore(m=m, height=500, width=1000, name="Neighborhoods",
                             column = "Land_Value", scheme = "quantiles", cmap = "RdYlBu_r", legend = True)
    return m

m = create_map('Berlin')
folium.LayerControl().add_to(m)
st_data = st_folium(m, width=725)

# Add a selectbox to the sidebar:
add_selectbox = st.sidebar.selectbox(
    'Stadt auswählen',
    ('Berlin', 'Bremen', 'Dresden', 'Franktfurt_am_Main', 'Köln')
)

