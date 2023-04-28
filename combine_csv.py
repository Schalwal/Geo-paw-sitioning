import pandas as pd
import glob
import os

def combine_csv(str_path):

    """
    Takes one argument: Full path of csv files
    """

    os.chdir(str_path)

    ls_files = glob.glob('*.{}'.format("csv"))
    ls_df = []

    if "Land Prices" in str_path:
            
        for file in ls_files:
            with open(file) as temp_file:
                ls_df.append(pd.read_csv(file, delimiter = ";"))

        return pd.concat(ls_df).drop(columns = ["Unnamed: 0"]).reset_index(drop = True)

    elif "Zensus" in str_path:

        for file in ls_files:

            with open(file) as temp_file:

                if "Berlin" in file:
                    df_temp = pd.read_csv(file, delimiter = ";")
                    df_temp["City"] = "Berlin"
                    df_temp["zensus_source"] = file.split("_")[-1].split(".")[0]
                    ls_df.append(df_temp)

                elif "Bremen" in file:
                    df_temp = pd.read_csv(file, delimiter = ";")
                    df_temp["City"] = "Bremen"
                    df_temp["zensus_source"] = file.split("_")[-1].split(".")[0]
                    ls_df.append(df_temp)

                elif "Dresden" in file:
                    df_temp = pd.read_csv(file, delimiter = ";")
                    df_temp["City"] = "Dresden"
                    df_temp["zensus_source"] = file.split("_")[-1].split(".")[0]
                    ls_df.append(df_temp)

                elif "Frankfurt_am_Main" in file:
                    df_temp = pd.read_csv(file, delimiter = ";")
                    df_temp["City"] = "Frankfurt_am_Main"
                    df_temp["zensus_source"] = file.split("_")[-1].split(".")[0]
                    ls_df.append(df_temp)

                elif "Köln" in file:
                    df_temp = pd.read_csv(file, delimiter = ";")
                    df_temp["City"] = "Köln"
                    df_temp["zensus_source"] = file.split("_")[-1].split(".")[0]
                    ls_df.append(df_temp)

                else:

                    pass

        return pd.concat(ls_df).drop(columns = ["Unnamed: 0"]).reset_index(drop = True)
    
    else:

        return "No appropriate folder to process"

    

#df_land_prices = combine_csv(input("Please copy + paste path to land prices: ").replace("\\", "/"))
#df_zensus = combine_csv(input("Please copy + paste path to land prices: ").replace("\\", "/"))