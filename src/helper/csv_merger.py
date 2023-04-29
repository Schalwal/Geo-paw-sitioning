import pandas as pd
import logging

import os

pd.options.mode.chained_assignment = None  # default='warn'


def combine_csvs(str_path: str) -> pd.DataFrame:
    """
    combines csv files at str_path and returns resulting DataFrame
    """

    # listing csv files in directory to be combined
    ls_files = [file for file in os.listdir(str_path) if file.endswith(".csv")]
    ls_df = []

    if "Land Prices" in str_path:
        for file in ls_files:
            ls_df.append(
                pd.read_csv(os.path.join(str_path, file), delimiter=";", index_col=0)
            )

        df_combined = pd.concat(ls_df).reset_index(drop=True)

        ls_categorial_columns = list(
            df_combined["Area_Types"]
            .str.split("_", expand=True)
            .value_counts()
            .index.values[0]
        )

        for col in ls_categorial_columns:
            df_combined[col] = 0

        df_categories_raw = df_combined["Area_Types"].str.split("_", expand=True)

        for i in range(len(df_combined)):
            df_categories_raw_row = df_categories_raw.iloc[i].dropna()

            for column in ls_categorial_columns:
                if column in df_categories_raw_row.values:
                    df_combined[column].iloc[i] += 1

        df_combined["City_Name"] = df_combined["City_Name"].str.replace("Frankfurt am Main", "Frankfurt_am_Main")

        return df_combined.drop(columns=["Area_Types"])

    elif "Zensus" in str_path:
        for file in ls_files:
            df_temp = pd.read_csv(os.path.join(str_path, file), delimiter=";")
            city_name = file.split("_")[1].split(".")[0]
            if "Frankfurt" in city_name:
                df_temp["City"] = "Frankfurt_am_Main"
            else:
                df_temp["City"] = file.split("_")[1].split(".")[0]
            df_temp["zensus_source"] = file.split("_")[-1].split(".")[0]
            ls_df.append(df_temp)

        return pd.concat(ls_df).drop(columns=["Unnamed: 0"]).reset_index(drop=True)
    else:
        logger.warn(
            "No appropriate directory to process at path:",
        )


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.WARN)

    main_path = os.getcwd()

    path_land = os.path.join(main_path, "res", "data", "DLR", "1 Land Prices")
    df_land_prices = combine_csvs(str_path=path_land)

    path_zensus = os.path.join(main_path, "res", "data", "DLR", "2 Zensus")
    df_zensus = combine_csvs(str_path=path_zensus)
