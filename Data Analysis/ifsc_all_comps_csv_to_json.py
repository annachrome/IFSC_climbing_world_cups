import pandas as pd
import json

wc_path = '/Users/apple/Documents/PROGRAMMING/Data Analysis/ifsc_data/worldcups_and_championships.csv'

# Specify column names since there's no header
column_names = ['event_id', 'comp_name', 'categories']

# Load the CSV file into a pandas DataFrame without headers and assign custom column names
df = pd.read_csv(wc_path, header=None, names=column_names)

# Convert the 'categories' column from a string representation of a list to an actual list
df['categories'] = df['categories'].apply(lambda x: eval(x))

# Convert the entire DataFrame to a JSON format
json_data = df.to_json(orient="records", date_format="iso")

# Save the JSON data to a file
with open("worldcups_and_championships.json", "w") as json_file:
    json_file.write(json_data)
