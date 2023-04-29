from sklearn import preprocessing
from sklearn.decomposition import PCA

import pandas as pd
import glob
import os
import numpy as np
import functools as ft


pd.options.mode.chained_assignment = None

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


def PCA_zensus_data(df_zensus, str_city, str_zensus_source):

    """
    Takes three arguments:
    1. DataFrame of the combined Zensus data
    2. City
    3. Type of Zensus Source


    Returns DataFrame with important factors with highest explained variance in single datasets
    """

    df_zensus_filtered_city_source = df_zensus[(df_zensus["City"] == str_city) & (df_zensus["zensus_source"] == str_zensus_source)].dropna(axis = 1).reset_index(drop = True)

    df_zensus_filtered = df_zensus_filtered_city_source.drop(columns = ["Grid_Code", "City", "zensus_source"])

    df_zensus_filtered_scaled = pd.DataFrame(preprocessing.scale(df_zensus_filtered),columns = df_zensus_filtered.columns) 

    pca_95 = PCA(n_components = 0.95, random_state = 2023)
    pca_95.fit(df_zensus_filtered_scaled)

    # number of components
    n_pcs = pca_95.components_.shape[0]

    # get the index of the most important feature on EACH component
    most_important = [np.abs(pca_95.components_[i]).argmax() for i in range(n_pcs)]
    initial_feature_names = df_zensus_filtered_scaled.columns.tolist()

    # get the names
    most_important_names = [initial_feature_names[most_important[i]] for i in range(n_pcs)]
    dic = {'PC{}'.format(i): most_important_names[i] for i in range(n_pcs)}

    # build the dataframe
    df_important_features = pd.DataFrame(dic.items()).rename(columns = {0 : "components", 1 : "features"})
    df_important_features["explained_variance"] = pca_95.explained_variance_ratio_ * 100
    df_important_features = df_important_features[["features", "explained_variance"]].groupby("features").sum().sort_values(by = "explained_variance", ascending = False).reset_index()

    return df_zensus_filtered_city_source, df_important_features


def combine_PCA_datasets(df_zensus, str_city):

    ls_zensus_sources = df_zensus["zensus_source"].unique()

    ls_pca_cleaned_zensus_data_city = []
    
    for source in ls_zensus_sources:
        
        df_zensus_filtered_city_source_original, important_features_city_source = PCA_zensus_data(df_zensus, str_city, source)
        
        df_zensus_filtered_city_source = df_zensus_filtered_city_source_original[df_zensus_filtered_city_source_original.columns.intersection(important_features_city_source["features"].tolist())]

        df_zensus_filtered_city_source["City"] = str_city
        df_zensus_filtered_city_source["Grid_Code"] = df_zensus_filtered_city_source_original["Grid_Code"]

        ls_pca_cleaned_zensus_data_city.append(df_zensus_filtered_city_source)

    
    df_cleaned = ft.reduce(lambda left, right: pd.merge(left, right, on = ['City', 'Grid_Code']), ls_pca_cleaned_zensus_data_city)

    return df_cleaned


if __name__ == "__main__":
    main_path = os.getcwd()
    df_land_prices = combine_csv(main_path + "/" +
        input("Please copy + paste path to land prices: ").replace("\\", "/") # main_path + "/" +
    )
    df_zensus = combine_csv(main_path + "/" +
        input("Please copy + paste path to zensus data: ").replace("\\", "/") # main_path + "/" +
    )

#    df_land_prices.to_csv(main_path + "/res/data/land_prices.csv")
#    df_zensus.to_csv(main_path + "/res/data/zensus.csv")

#df_zensus_berlin = combine_PCA_datasets(df_zensus, "Berlin") 
#df_zensus_bremen = combine_PCA_datasets(df_zensus, "Bremen") 
#df_zensus_dresden = combine_PCA_datasets(df_zensus, "Dresden") 
#df_zensus_frankfurt = combine_PCA_datasets(df_zensus, "Frankfurt") 
#df_zensus_koeln = combine_PCA_datasets(df_zensus, "Köln")