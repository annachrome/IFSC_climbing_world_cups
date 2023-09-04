#  combine csv files, 
# filter out world cups and championships, 
# use urls to scrape results,

import pandas as pd
import requests
import json
import logging

logging.basicConfig(
    filename='ifsc_results_scraper_log.txt',
      level=logging.INFO, 
      format='%(asctime)s:%(levelname)s:%(message)s'
      )

base_url = 'https://components.ifsc-climbing.org/results-api.php?api=event_full_results&result_url='
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
}

def fetch_results(endpoint):
    """Fetch results from given endpoint"""
    full_url = base_url + endpoint


    try:
        response = requests.get(full_url, headers=headers)
        response.raise_for_status()  # raises HTTPError if HTTP request returned unsuccessful status code
        print(f"Fetching results from {full_url}")
        return response.json()  # Convert to JSON
    except requests.RequestException as e:
        print("RequestException Error:", e) # Add this
        logging.error(f"Error fetching results from {full_url}: {e}")
        return None
    except json.JSONDecodeError:
        print("JSONDecodeError") # And this
        logging.error(f"Error decoding JSON from {full_url}")
        return None

def main():
    raw_df = '/Users/apple/Documents/PROGRAMMING/Data Analysis/ifsc_data/worldcups_and_championships.json' 
    raw_df = pd.read_json(raw_df) #0: event_id, 1: comp_name, 2: comp

    all_comps = {
        'LEAD Women': pd.DataFrame(),
        'BOULDER Women': pd.DataFrame(),
        'COMBINED Women': pd.DataFrame(),
        'BOULDER&LEAD Women': pd.DataFrame(),
    }

    for i, row in raw_df.iterrows():

        try:
            comp_name = row.iloc[1]
            wc_json = row.iloc[2]

            for comp_dict in wc_json: # for each {e.g. lead W} comp in {e.g. Innsbruk 2018}

                results_url = comp_dict['results_url']
                comp_scraped = fetch_results(results_url)

                if comp_scraped:
                    new_row = {
                        'comp_name': comp_name,
                        'results': comp_scraped 
                    }

                    # Check if the category is in all_comps
                    if comp_dict['category'] in all_comps:
                        # Convert new_row to a DataFrame and append it to the existing DataFrame
                        temp_df = pd.DataFrame([new_row])
                        all_comps[comp_dict['category']] = pd.concat([all_comps[comp_dict['category']], temp_df], ignore_index=True)

        except Exception as e:
            print((f"Unexpected error processing row {row}: {e}"))
            logging.error(f"Unexpected error processing row {row}: {e}")

    all_comps['LEAD Women'].to_json('/Users/apple/Documents/PROGRAMMING/Data Analysis/ifsc_data/Wlead.json', index=False)
    all_comps['BOULDER Women'].to_json('/Users/apple/Documents/PROGRAMMING/Data Analysis/ifsc_data/Wboulder.json', index=False)
    all_comps['COMBINED Women'].to_json('/Users/apple/Documents/PROGRAMMING/Data Analysis/ifsc_data/Wcombined.json', index=False)
    all_comps['BOULDER&LEAD Women'].to_json('/Users/apple/Documents/PROGRAMMING/Data Analysis/ifsc_data/Wboulderlead.json', index=False)

if __name__ == "__main__":
    main()