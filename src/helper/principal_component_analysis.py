import os

import pandas as pd
import geopandas as gpd
import numpy as np
import functools as ft

from sklearn import preprocessing
from sklearn.decomposition import PCA

from helper.csv_merger import combine_csvs


def PCA_zensus_data(
    df_zensus: pd.DataFrame, str_city: str, str_zensus_source: str
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Returns result of PCA features of zensus data.

            Parameters:
                    df_zensus (pd.DataFrame): DataFrame for zensus data
                    str_city (str): String of city name
                    str_zensus_source (str): String of zensus source

            Returns:
                    df_zensus_filtered_city_source, df_important_features (tuple): dataframe on city and source level, and dataframe pca result
    """

    df_zensus_filtered_city_source = (
        df_zensus[
            (df_zensus["City"] == str_city)
            & (df_zensus["zensus_source"] == str_zensus_source)
        ]
        .dropna(axis=1)
        .reset_index(drop=True)
    )

    df_zensus_filtered = df_zensus_filtered_city_source.drop(
        columns=["Grid_Code", "City", "zensus_source"]
    )

    df_zensus_filtered_scaled = pd.DataFrame(
        preprocessing.scale(df_zensus_filtered), columns=df_zensus_filtered.columns
    )

    pca_95 = PCA(n_components=0.95, random_state=2023)
    pca_95.fit(df_zensus_filtered_scaled)

    # number of components
    n_pcs = pca_95.components_.shape[0]

    # get the index of the most important feature on EACH component
    most_important = [np.abs(pca_95.components_[i]).argmax() for i in range(n_pcs)]
    initial_feature_names = df_zensus_filtered_scaled.columns.tolist()

    # get the names
    most_important_names = [
        initial_feature_names[most_important[i]] for i in range(n_pcs)
    ]
    dic = {"PC{}".format(i): most_important_names[i] for i in range(n_pcs)}

    # build the dataframe
    df_important_features = pd.DataFrame(dic.items()).rename(
        columns={0: "components", 1: "features"}
    )
    df_important_features["explained_variance"] = pca_95.explained_variance_ratio_ * 100
    df_important_features = (
        df_important_features[["features", "explained_variance"]]
        .groupby("features")
        .sum()
        .sort_values(by="explained_variance", ascending=False)
        .reset_index()
    )

    return df_zensus_filtered_city_source, df_important_features


def combine_PCA_datasets(df_zensus, str_city, str_path):
    """
    returns the combination of zensus data for city and all sources based on PCA
    """

    ls_files_gpkg = [
        file
        for file in os.listdir(str_path)
        if file.endswith(".gpkg") and str_city in file
    ]
    

    zensus_grid = gpd.read_file(os.path.join(str_path, ls_files_gpkg[0]))

    ls_zensus_sources = df_zensus["zensus_source"].unique()

    ls_pca_cleaned_zensus_data_city = []

    # Filter original zensus Dataframe by only looking at the columns that are relevant due to the PCA

    for source in ls_zensus_sources:
        (
            df_zensus_filtered_city_source_original,
            important_features_city_source,
        ) = PCA_zensus_data(df_zensus, str_city, source)

        df_zensus_filtered_city_source = df_zensus_filtered_city_source_original[
            df_zensus_filtered_city_source_original.columns.intersection(
                important_features_city_source["features"].tolist()
            )
        ]

        df_zensus_filtered_city_source["City"] = str_city
        df_zensus_filtered_city_source[
            "Grid_Code"
        ] = df_zensus_filtered_city_source_original["Grid_Code"]

        ls_pca_cleaned_zensus_data_city.append(df_zensus_filtered_city_source)

    # combine with geodata

    df_cleaned = ft.reduce(
        lambda left, right: pd.merge(left, right, on=["City", "Grid_Code"]),
        ls_pca_cleaned_zensus_data_city,
    )

    idx_column = "Grid_Code"
    zensus_grid = zensus_grid.merge(df_cleaned, on=idx_column, how="inner")

    return zensus_grid


if __name__ == "__main__":
    main_path = os.getcwd()
    path_zensus = os.path.join(main_path, "res", "data", "DLR", "2 Zensus")
    df_zensus = combine_csvs(str_path=path_zensus)

    cities = ["Berlin", "Bremen", "Dresden", "Frankfurt_am_Main", "Köln"]
    """for city in cities:
        df_zensus = combine_PCA_datasets(df_zensus, city)"""
    df_zensus = combine_PCA_datasets(
        df_zensus=df_zensus, str_city=cities[0], str_path=path_zensus
    )
