from bs4 import BeautifulSoup as bs
import requests
import re
import json
import csv

base_url = 'https://components.ifsc-climbing.org/results-api.php'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
}

all_data = []
chunk_size = 100 # save to csv every n instances

for event_id in range(0, 937): # 937: first 2015 WC, 1301: 2023 world champs in aug
    params = {
        'api': 'event_results',
        'event_id': event_id
    }

    response = requests.get(base_url, params=params, headers=headers)

    if response.status_code == 200:
        response_content = response.text
        valid_json_start = response_content.find('{')  # Assuming the JSON data always starts with '{'
        cleaned_content = response_content[valid_json_start:]

        if valid_json_start != -1:
            try:
                print(event_id)
                data = json.loads(cleaned_content) 
                categories = []
                
                if 'd_cats' in data:
                    for dict in data['d_cats']:
                        cat_entry = {
                            'category': dict['dcat_name'],
                            'results_url': dict['full_results_url'],
                        }
                        categories.append(cat_entry)
                if 'name' not in data:
                    name = None
                    print(f"KeyError for event_id: {event_id}. Missing key: 'name'.")
                else:
                    name = data['name']

                entry = {
                    'event_id': event_id,
                    'event_name': name,
                    'categories_list': categories,
                }
                all_data.append(entry)
            except json.JSONDecodeError:
                print(f"Invalid JSON response for event_id: {event_id}")
                print(cleaned_content)
    else:
        print(f"Failed to fetch data for event_id: {event_id}")

    if len(all_data) == chunk_size:
        #print(entry)
        with open(f'/Users/apple/Documents/PROGRAMMING/Data Analysis/ifsc_data/{event_id}_onwards.csv', 'w', newline='') as csvfile:
            fieldnames = ['event_id', 'event_name', 'categories_list']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in all_data:
                writer.writerow(row)
        
        all_data = []  # Clear the data



if all_data:
    with open(f'/Users/apple/Documents/PROGRAMMING/Data Analysis/ifsc_data/{event_id}_final_chunk.csv', 'w', newline='') as csvfile:
        fieldnames = ['event_id', 'event_name', 'categories_list']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in all_data:
            writer.writerow(row)

