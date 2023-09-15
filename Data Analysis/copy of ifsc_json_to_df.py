# convert jsons to pd df

import pandas as pd
import json
import logging
import re

paths = [
    #'/Users/apple/Documents/PROGRAMMING/IFSC_climbing_world_cups/Data Analysis/ifsc_data/Wlead.json',
    # '/Users/apple/Documents/PROGRAMMING/IFSC_climbing_world_cups/Data Analysis/ifsc_data/Wboulder.json',
    # '/Users/apple/Documents/PROGRAMMING/IFSC_climbing_world_cups/Data Analysis/ifsc_data/Wcombined.json',
    # '/Users/apple/Documents/PROGRAMMING/IFSC_climbing_world_cups/Data Analysis/ifsc_data/Wboulderlead.json',
]
dir = '/Users/apple/Documents/PROGRAMMING/IFSC_climbing_world_cups/Data Analysis/ifsc_data/'

logging.basicConfig(
    filename=dir + 'ifsc_results_scraper_log.txt',
      level=logging.INFO, 
      format='%(asctime)s:%(levelname)s:%(message)s'
      )

def cell_is_json(cell):
    """
    checks if a cell is a string containing json info
    returns True/False
    """
    if not (isinstance(cell, list) or isinstance(cell, str)):  # Only process string cells
        return False
    
    #logging.info(f"{cell} is type list and might be json")
    try:
        cell = str(cell)
        cell = cell.replace("True", "true").replace("False", "false").replace("None","null").replace("\\xa","_")
        cell = replace_single_quotes(cell)

        if not (cell.startswith('{') and cell.endswith('}')) and not (cell.startswith('[') and cell.endswith(']')):
            return False
        
        json.loads(cell)
        return True
    
    except json.JSONDecodeError:
        #logging.error(f"is_json function had json.JSONDecodeError for cell {cell}.")
        return False
    
def unique_datatypes(df, column_name):
    """
    Identify unique datatypes in a given column of a DataFrame.

    Parameters:
    - df (pd.DataFrame): The DataFrame to inspect.
    - column_name (str): The name of the column to check.

    Returns:
    - set: A set of unique datatypes in the specified column.
    """
    return set(df[column_name].map(type))

def ifsc_json_to_csv(data, out_path):
    """
    data is df from pd.read_json(some_json_file)
    """
    ranking_depth_1 = pd.DataFrame()

    try:
        for _, row in data.iterrows():
            # Normalize the 'ranking' list of dictionaries
            df_temp = pd.json_normalize(row['results']['ranking'])
            
            # Add the 'comp_name' column to the temporary DataFrame
            df_temp['comp_name'] = row['comp_name']
            
            # Append the temporary DataFrame to the ranking_depth_1 DataFrame
            ranking_depth_1 = pd.concat([ranking_depth_1, df_temp], ignore_index=True)

        ranking_depth_1.to_csv(out_path, index=False)

        return ranking_depth_1 
    
    except Exception as e:
        logging.error(f"ifsc_json_to_csv had error: \n {e}")

def replace_single_quotes(str):
    """
    make string json-format before converting to json
    """
    return str.replace("{'", '{"').replace("': ", '": ').replace(": '", ': "').replace("', ", '", ').replace(", '", ', "').replace("'}", '"}')

def normalize_depth(data, json_columns):
    """
    takes dataframe 'data' and list of str column names that has jsons as strings
    returns dataframe with normalize/de-nested json as separate columns"""
    df_output = pd.DataFrame()
    length = len(data)

    for idx, row in data.iterrows():
        print(f"processing row {idx+1} of {length}")
        
        for json_col in json_columns:

            if json_col not in data.columns or not row[json_col] or not cell_is_json(str(row[json_col])):
                df_output = pd.concat([df_output, pd.DataFrame([row])], ignore_index=True)
            else:
                try:
                    row_str = row[json_col].replace("True", "true").replace("False", "false").replace("None","null").replace("\\xa","_")
                    row_str = replace_single_quotes(row_str)
                    row_json = json.loads(row_str)

                    df_temp = pd.json_normalize(row_json)

                    row_data = row.drop(json_col)
                    
                    for col, value in row_data.items():
                        df_temp[col] = value

                    df_output = pd.concat([df_output, df_temp], ignore_index=True)

                except Exception as e:
                    logging.error(f"row_str has type {type(row_str)} \n{row_str} \n Error: \n {e} \n")
                    df_output = pd.concat([df_output, pd.DataFrame([row])], ignore_index=True)


    return df_output

def main():
    category = 'Wboulder'

    data = pd.read_csv(dir + category + "_2.csv")
    data.replace("[]", "", inplace=True)
    #6 checking
    # data = pd.read_csv(dir + category + ".csv")

    #checks for all data
    print(data.head())
    unique_dtypes_dict = {
        col: unique_datatypes(data, col) for col in data.columns
    }
    logging.info(f"unique dtypes of each column are {unique_dtypes_dict}")


    json_cells = data.map(cell_is_json, na_action='ignore')

    # gives both parent and nested/child columns
    all_json_columns = json_cells.columns[json_cells.any()].tolist()

    # only child columns
    json_columns = [col for col in all_json_columns if not any(c.startswith(f"{col}.") for c in all_json_columns)]
    logging.info(f"json columns in str type needing unpacking are {json_columns}")
    print(f"json columns in str type needing unpacking are {json_columns}")


    #4 EDIT OUTPUT PATH AS NEEDED
    # ascents_depth_4 = normalize_depth(data, json_columns)
    # ascents_depth_4.to_csv(dir + category + '_2.csv')

    logging.info("csv written")

if __name__ == "__main__":
    main()

