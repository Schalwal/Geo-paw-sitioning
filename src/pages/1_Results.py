import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image
import random
import os

st.set_option('deprecation.showPyplotGlobalUse', False)

st.set_page_config(page_title="Geo-'Paw'-Sitioning", 
                   page_icon=None, 
                   layout="wide", 
                   initial_sidebar_state="auto",
                   menu_items=None)


#df_berlin = pd.read_csv("D:/GitHub/Geo-paw-sitioning/res/data/Geo-paw-sitioningBerlin.csv").drop(columns = ["geometry", "City_Name", "City_Code", "index_right", "Neighborhood_FID", "District_Name"])
#df_bremen = pd.read_csv("D:/GitHub/Geo-paw-sitioning/res/data/Geo-paw-sitioningBremen.csv").drop(columns = ["geometry", "City_Name", "City_Code", "index_right", "Neighborhood_FID", "District_Name", "Neighborhood_Code", "District_Code"])
#df_dresden = pd.read_csv("D:/GitHub/Geo-paw-sitioning/res/data/Geo-paw-sitioningDresden.csv").drop(columns = ["geometry", "City_Name", "City_Code", "index_right", "Neighborhood_FID", "Neighborhood_Code"])
#df_frankfurt = pd.read_csv("D:/GitHub/Geo-paw-sitioning/res/data/Geo-paw-sitioningFrankfurt_am_Main.csv").drop(columns = ["geometry", "City_Name", "City_Code", "Neighborhood_FID"])
#df_koeln = pd.read_csv("D:/GitHub/Geo-paw-sitioning/res/data/Geo-paw-sitioningKöln.csv").drop(columns = ["geometry", "City_Name", "City_Code", "Neighborhood_FID", "District_Name"])
#
#berlin_coeff = pd.read_csv("D:/GitHub/Geo-paw-sitioning/res/data/Berlin_coeff.csv").sort_values("Coeff", ascending=False)
#bremen_coeff = pd.read_csv("D:/GitHub/Geo-paw-sitioning/res/data/Bremen_coeff.csv").sort_values("Coeff", ascending=False)
#dresden_coeff = pd.read_csv("D:/GitHub/Geo-paw-sitioning/res/data/Dresden_coeff.csv").sort_values("Coeff", ascending=False)
#frankfurt_coeff = pd.read_csv("D:/GitHub/Geo-paw-sitioning/res/data/Frankfurt_coeff.csv").sort_values("Coeff", ascending=False)
#koeln_coeff = pd.read_csv("D:/GitHub/Geo-paw-sitioning/res/data/Koeln_coeff.csv").sort_values("Coeff", ascending=False)

df_berlin = pd.read_csv("../res/data/Geo-paw-sitioningBerlin.csv").drop(columns = ["geometry", "City_Name", "City_Code", "index_right", "Neighborhood_FID", "District_Name"])
df_bremen = pd.read_csv("../res/data/Geo-paw-sitioningBremen.csv").drop(columns = ["geometry", "City_Name", "City_Code", "index_right", "Neighborhood_FID", "District_Name", "Neighborhood_Code", "District_Code"])
df_dresden = pd.read_csv("../res/data/Geo-paw-sitioningDresden.csv").drop(columns = ["geometry", "City_Name", "City_Code", "index_right", "Neighborhood_FID", "Neighborhood_Code"])
df_frankfurt = pd.read_csv("../res/data/Geo-paw-sitioningFrankfurt_am_Main.csv").drop(columns = ["geometry", "City_Name", "City_Code", "Neighborhood_FID"])
df_koeln = pd.read_csv("../res/data/Geo-paw-sitioningKöln.csv").drop(columns = ["geometry", "City_Name", "City_Code", "Neighborhood_FID", "District_Name"])

berlin_coeff = pd.read_csv("../res/data/Berlin_coeff.csv").sort_values("Coeff", ascending=False)
bremen_coeff = pd.read_csv("../res/data/Bremen_coeff.csv").sort_values("Coeff", ascending=False)
dresden_coeff = pd.read_csv("../res/data/Dresden_coeff.csv").sort_values("Coeff", ascending=False)
frankfurt_coeff = pd.read_csv("../res/data/Frankfurt_coeff.csv").sort_values("Coeff", ascending=False)
koeln_coeff = pd.read_csv("../res/data/Koeln_coeff.csv").sort_values("Coeff", ascending=False)

sns.set(font_scale=2)

corr_berlin = np.corrcoef(df_berlin)
fig_corr_berlin = plt.figure(figsize=(30,20))
sns.heatmap(corr_berlin, 
        xticklabels=df_berlin.columns,
        yticklabels=df_berlin.columns)

fig_coeff_berlin = plt.figure(figsize=(30,20))
sns.barplot(data=berlin_coeff, x="Name", y="Coeff")

corr_bremen = np.corrcoef(df_bremen)
fig_corr_bremen = plt.figure(figsize=(30,20))
sns.heatmap(corr_bremen, 
        xticklabels=df_bremen.columns,
        yticklabels=df_bremen.columns)

fig_coeff_bremen = plt.figure(figsize=(30,20))
sns.barplot(data=bremen_coeff, x="Name", y="Coeff")

corr_dresden = np.corrcoef(df_dresden)
fig_corr_dresden = plt.figure(figsize=(30,20))
sns.heatmap(corr_dresden, 
        xticklabels=df_dresden.columns,
        yticklabels=df_dresden.columns)

fig_coeff_dresden = plt.figure(figsize=(30,20))
sns.barplot(data=dresden_coeff, x="Name", y="Coeff")

corr_frankfurt = np.corrcoef(df_frankfurt)
fig_corr_frankfurt = plt.figure(figsize=(30,20))
sns.heatmap(corr_frankfurt, 
        xticklabels=df_frankfurt.columns,
        yticklabels=df_frankfurt.columns)

fig_coeff_frankfurt = plt.figure(figsize=(30,20))
sns.barplot(data=frankfurt_coeff, x="Name", y="Coeff")

corr_koeln = np.corrcoef(df_koeln)
fig_corr_koeln = plt.figure(figsize=(30,20))
sns.heatmap(corr_koeln, 
        xticklabels=df_koeln.columns,
        yticklabels=df_koeln.columns)

fig_coeff_koeln = plt.figure(figsize=(30,20))
sns.barplot(data=koeln_coeff, x="Name", y="Coeff")


#left_column, right_column = st.columns([1,1])



# Add a selectbox to the sidebar:
city_choice2 = st.sidebar.selectbox(
    key='city',
    label='Choose City',
    options=('Berlin', 'Bremen', 'Dresden', 'Frankfurt_am_Main', 'Köln')
)

#image_paths = os.listdir("D:/GitHub/Geo-paw-sitioning/res/streamlit/images/")
#image = Image.open('D:/GitHub/Geo-paw-sitioning/res/streamlit/images/' + image_paths[random.randint(0, len(image_paths) - 1)])
image_paths = os.listdir("../res/streamlit/images/")
image = Image.open('../res/streamlit/images/' + image_paths[random.randint(0, len(image_paths) - 1)])
st.sidebar.image(image, caption='Cat')

#with left_column:

if city_choice2 == 'Berlin':
    st.pyplot(fig_coeff_berlin)
    #image_reg = Image.open('D:/GitHub/Geo-paw-sitioning/res/data/Berlin_reg_results.png')
    image_reg = Image.open('../res/data/Berlin_reg_results.png')
    st.image(image_reg)  

if city_choice2 == 'Bremen':
    st.pyplot(fig_coeff_bremen)

if city_choice2 == 'Dresden':
    st.pyplot(fig_coeff_dresden)

if city_choice2 == 'Frankfurt_am_Main':
    st.pyplot(fig_coeff_frankfurt)

if city_choice2 == 'Köln':
    st.pyplot(fig_coeff_koeln)


if city_choice2 == 'Berlin':
    st.pyplot(fig_corr_berlin)

if city_choice2 == 'Bremen':
    st.pyplot(fig_corr_bremen)

if city_choice2 == 'Dresden':
    st.pyplot(fig_corr_dresden)

if city_choice2 == 'Frankfurt_am_Main':
    st.pyplot(fig_corr_frankfurt)

if city_choice2 == 'Köln':
    st.pyplot(fig_corr_koeln)

#with right_column:



