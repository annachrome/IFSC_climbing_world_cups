# convert jsons to pd df

import pandas as pd
import json

paths = [
    '/Users/apple/Documents/PROGRAMMING/IFSC_climbing_world_cups/Data Analysis/ifsc_data/Wlead.json',
    # '/Users/apple/Documents/PROGRAMMING/IFSC_climbing_world_cups/Data Analysis/ifsc_data/Wboulder.json',
    # '/Users/apple/Documents/PROGRAMMING/IFSC_climbing_world_cups/Data Analysis/ifsc_data/Wcombined.json',
    # '/Users/apple/Documents/PROGRAMMING/IFSC_climbing_world_cups/Data Analysis/ifsc_data/Wboulderlead.json',
]

path = '/Users/apple/Documents/PROGRAMMING/IFSC_climbing_world_cups/Data Analysis/ifsc_data/Wlead_df.csv'
out_path = '/Users/apple/Documents/PROGRAMMING/IFSC_climbing_world_cups/Data Analysis/ifsc_data/Wlead_ascents.csv'



def normalize_depth(data, key_col, drop_col):
    df_output = pd.DataFrame()

    for index, row in data.iterrows():
        # Check if key_col exists and is not null
        
        if key_col in data.columns:
            if row[key_col]:
                if type(row[key_col]) == str:
                    row_str = row[key_col].replace("'", '"').replace("True", "true").replace("False", "false").replace("None","null")
                    print(type(row_str))
                    print(row_str)
                    row_json = json.loads(row_str)
                    
                    df_temp = pd.json_normalize(row_json)

                    row_data = row.drop(drop_col)

                    for col, value in row_data.items():
                        df_temp[col] = value

                    df_output = pd.concat([df_output, df_temp], ignore_index=True)
                else:
                    print(type(row[key_col]))
                    print(row[key_col])
        else:
            df_output = pd.concat([df_output, row], ignore_index=True)

    return df_output

#data = pd.read_json(path)

# ranking_depth_1 = normalize_depth(data, 'results.ranking', 'results')
# print(ranking_depth_1.head())

# round_depth_2 = normalize_depth(ranking_depth_1, 'rounds', 'rounds')
# print(round_depth_2.head())

# ascents_depth_3 = normalize_depth(round_depth_2, 'ascents', 'ascents')
# print(ascents_depth_3.head())


data = pd.read_csv(path)

ascents_depth_3 = normalize_depth(data, 'ascents', 'ascents')
print(ascents_depth_3.head())

ascents_depth_3.to_csv(out_path, index=False)





# # Create an empty DataFrame to hold the normalized results
# ranking_depth_1 = pd.DataFrame()

# # Iterate over each row in the data
# for index, row in data.iterrows():
#     # Normalize the 'ranking' list of dictionaries
#     df_temp = pd.json_normalize(row['results']['ranking'])
    
#     # Add the 'comp_name' column to the temporary DataFrame
#     df_temp['comp_name'] = row['comp_name']
    
#     # Append the temporary DataFrame to the ranking_depth_1 DataFrame
#     ranking_depth_1 = pd.concat([ranking_depth_1, df_temp], ignore_index=True)

# print(ranking_depth_1.head())

# # Now, further normalize the 'rounds' column
# round_depth_2 = pd.DataFrame()

# for index, row in ranking_depth_1.iterrows():
#     # Check if 'rounds' exists and is not null
#     if ('rounds' in ranking_depth_1.columns) and (pd.notnull(row['rounds']).any()):
#         df_temp = pd.json_normalize(row['rounds'])
        
#         row_data = row.drop('rounds')
        
#         for col, value in row_data.items():
#             df_temp[col] = value

#         round_depth_2 = pd.concat([round_depth_2, df_temp], ignore_index=True)
#     else:
#         round_depth_2 = pd.concat([round_depth_2, df_temp], ignore_index=True)

# print(round_depth_2.head())


# # Now, further normalize the 'ascents' column
# ascents_depth_3 = pd.DataFrame()

# for index, row in round_depth_2.iterrows():
#     # Check if 'rounds' exists and is not null
#     if ('ascents' in round_depth_2.columns) and (pd.notnull(row['ascents']).any()):
#         df_temp = pd.json_normalize(row['ascents'])
        
#         row_data = row.drop('ascents')
        
#         for col, value in row_data.items():
#             df_temp[col] = value

#         ascents_depth_3 = pd.concat([ascents_depth_3, df_temp], ignore_index=True)
#     else:
#         ascents_depth_3 = pd.concat([ascents_depth_3, df_temp], ignore_index=True)

# print(ascents_depth_3.head())


