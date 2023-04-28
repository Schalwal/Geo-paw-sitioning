import pandas as pd
import glob
import os


def combine_csv(str_path):
    """
    Takes one argument: Full path of csv files
    """

    os.chdir(str_path)

    ls_files = glob.glob("*.{}".format("csv"))
    ls_df = []

    if "Land Prices" in str_path:
        for file in ls_files:
            ls_df.append(pd.read_csv(file, delimiter=";"))

        return pd.concat(ls_df).drop(columns=["Unnamed: 0"]).reset_index(drop=True)

    elif "Zensus" in str_path:
        for file in ls_files:
            df_temp = pd.read_csv(file, delimiter=";")
            df_temp["City"] = file.split("_")[1].split(".")[0]
            df_temp["zensus_source"] = file.split("_")[-1].split(".")[0]
            ls_df.append(df_temp)

        return pd.concat(ls_df).drop(columns=["Unnamed: 0"]).reset_index(drop=True)

    else:
        return "No appropriate folder to process"


if __name__ == "__main__":
    df_land_prices = combine_csv(
        input("Please copy + paste path to land prices: ").replace("\\", "/")
    )
    df_zensus = combine_csv(
        input("Please copy + paste path to zensus data: ").replace("\\", "/")
    )
