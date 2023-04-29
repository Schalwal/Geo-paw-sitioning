import streamlit as st
import os
import glob
import numpy as np
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium, folium_static
from shapely import wkt

# streamlit run Start.py

st.set_page_config(page_title="Geo-'Paw'-Sitioning", 
                   page_icon=None, 
                   layout="wide", 
                   initial_sidebar_state="auto",
                   menu_items=None)

@st.cache_data
def read_features(city):
    df = pd.read_csv("D:/GitHub/Geo-paw-sitioning/res/data/" + "land_prices.csv")
    #df = pd.read_csv("D:/GitHub/Geo-paw-sitioning/res/data/DLR/1 Land Prices/Land_Prices_Neighborhood_" + city + ".csv", sep=";")
    #df = df.drop(columns=['Area_Count',"geometry", "Unnamed: 0", "Neighborhood_Name", "District_Name", "City_Code", "City_Name"])
    df = df.drop(columns=["Unnamed: 0"])
    return df 

@st.cache_data
def read_geo(city):
    df_geo = gpd.read_file("D:/GitHub/Geo-paw-sitioning/res/data/DLR/1 Land Prices/Land_Prices_Neighborhood_" + city + ".gpkg")
    #df_geo = df_geo.drop(columns = ['Area_Types', 'Area_Count', 'City_Name'])
    return df_geo

@st.cache_data
def merge_frames(df_csv, _df_geo):
    df_geo_merged = gpd.GeoDataFrame(df_csv, geometry=_df_geo["geometry"]) 
    df_geo_merged = df_geo_merged[df_geo_merged.geom_type == 'MultiPolygon']
    return df_geo_merged


def create_map(city, features):
    df_csv = read_features(city)
    df_geo = read_geo(city)
    df_geo_merged = merge_frames(df_csv, df_geo)
    m = df_geo_merged.explore(
        name="Land_Value", 
        column= "Land_Value", 
        width = 1200, 
        height = 600, 
        legend = False,
        tooltip = False
    )

    #if(len(features) == 0):
    #    return m    
    for feature in features:
        m = df_geo_merged.explore(m = m, name=feature,
                                column = feature, scheme = "quantiles", cmap = "RdYlBu_r", legend = False, 
                                tooltip_kwds = {"labels": False})   
    
    return m



# Add a selectbox to the sidebar:
city_choice = st.sidebar.selectbox(
    key='city',
    label='Choose City',
    options=('Berlin', 'Bremen', 'Dresden', 'Frankfurt_am_Main', 'Köln')
)

features = st.sidebar.multiselect(
    'Choose Features',
    set(read_features(city_choice).columns) - set(["Neighborhood_FID", "Land_Value"])
    #["v1", "v2", "v3"]
)

left_column, right_column = st.columns([4,1])

with left_column:
    #st.write(merge_frames(read_features(city_choice), read_geo(city_choice)).columns)
    m = create_map(city_choice, features)
    folium.LayerControl(position = "topleft").add_to(m)
    st_data = st_folium(m, width = 1200, height = 1000)

    #st.write(read_features(city_choice))
    #st.write(read_geo(city_choice))



with right_column:
    #st.write(st_data)    
    try:
        st.write(st_data["last_active_drawing"]["properties"])
    except:
        st.write({"Please select a cell:"})
