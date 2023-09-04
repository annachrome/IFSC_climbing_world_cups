from bs4 import BeautifulSoup as bs
import requests
import re
import json
import csv

event_id = 1087
all_data = []

base_url = 'https://components.ifsc-climbing.org/results-api.php'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
}
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

            entry = {
                'event_id': data['id'],
                'event_name': data['name'],
                'categories_list': categories,
            }
            all_data.append(entry)

        except json.JSONDecodeError:
            print(f"Invalid JSON response for event_id: {event_id}")
            print(cleaned_content)
        except KeyError as ke:
            print(f"KeyError for event_id: {event_id}. Missing key: {ke}")
            print(cleaned_content)

else:
    print(f"Failed to fetch data for event_id: {event_id}")


