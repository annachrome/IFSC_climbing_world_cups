# take raw data and clean for feature engineering: remove None rows, re-format weird symbols

import pandas as pd
import logging
from datetime import datetime

def main():
    category = "Wlead
    "

    dir = '/Users/apple/Documents/PROGRAMMING/IFSC_climbing_world_cups/Data Analysis/ifsc_data/'

    #current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    logging.basicConfig(
        filename=dir + f'ifsc_cleaning_log.txt',
        level=logging.INFO, 
        format='%(asctime)s:%(levelname)s:%(message)s'
        )

    data = pd.read_csv(dir + category + ".csv")

    mono_cols_dict = {col: data[col].iloc[0] for col in data.columns if data[col].nunique() == 1}
    none_cols_dict = {col: None for col in data.columns if data[col].isnull().all()}
    unnamed_cols_dict = {col: data[col].unique() for col in data.columns if "Unnamed" in col}

    logging.info(f"\nUnnamed columns: \n{unnamed_cols_dict} \n\n Single value columns: \n {mono_cols_dict} \n\n Empty columns: {none_cols_dict}\n")

    delete_cols_dict = {**mono_cols_dict, **none_cols_dict, **unnamed_cols_dict}         

    output = '\n'.join(f"{key}: {value}" for key, value in delete_cols_dict.items())
    input_string = input(
        f"Which columns should NOT be deleted out of these columns? Input the column names separated by commas. \n\n {output}\n\n"
        )

    except_cols_list = [column_name.strip().replace('"', '').replace("'", "") for column_name in input_string.split(",")]

    drop_cols = [key for key in delete_cols_dict if key not in except_cols_list]
    
    data.drop(columns=drop_cols, inplace=True)
    deduplicated = data.drop_duplicates()
    deduplicated.to_csv(dir + category + "_cleaned.csv")

if __name__ == "__main__":
    main()
    





