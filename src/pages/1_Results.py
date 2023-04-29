import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_option('deprecation.showPyplotGlobalUse', False)

st.set_page_config(page_title="Geo-'Paw'-Sitioning", 
                   page_icon=None, 
                   layout="wide", 
                   initial_sidebar_state="auto",
                   menu_items=None)

#def plot_example():
#    titanic = sns.load_dataset("titanic")
#    fig = plt.figure(figsize=(10, 4))
#    sns.countplot(x="class", data=titanic)
#    
#    #return fig

#st.pyplot(plot_example())

df_berlin = pd.read_csv("D:/GitHub/Geo-paw-sitioning/res/data/Geo-paw-sitioningBerlin.csv").drop(columns = ["geometry", "City_Name", "City_Code", "index_right", "Neighborhood_FID", "District_Name"])

corr = np.corrcoef(df_berlin)
fig_berlin = plt.figure(figsize=(30,20))
sns.heatmap(corr, 
        xticklabels=df_berlin.columns,
        yticklabels=df_berlin.columns)


left_column, right_column = st.columns([1,1])

# Add a selectbox to the sidebar:
city_choice2 = st.sidebar.selectbox(
    key='city',
    label='Choose City',
    options=('Berlin', 'Bremen', 'Dresden', 'Frankfurt_am_Main', 'Köln')
)

with left_column:
    if city_choice2 == 'Berlin':
        st.pyplot(fig_berlin)

with right_column:
    if city_choice2 == 'Berlin':
        st.pyplot(fig_berlin)

