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

titanic = sns.load_dataset("titanic")

fig = plt.figure(figsize=(10, 4))
sns.countplot(x="class", data=titanic)

st.pyplot(fig)


titanic = sns.load_dataset("titanic")

fig2 = plt.figure(figsize=(10, 4))
sns.countplot(x="class", data=titanic)

st.pyplot(fig2)

