# Order of execution:

- **File:** `ifsc_results_scraping.py`
  - **Description:** Step 1/5 in IFSC scraping
  - **Scrapes:** 
    - `event_id`
    - `comp_name`
    - `category`
    - `results_url`
  - **Outputs:** Data in 100-piece chunks into `{event_id}_onwards.csv` files and the last few results into `{event_id}_final_chunk.csv`

- **Undocumented:**
    - Step 2/5 in IFSC scraping 
    - Merge csv files into a single worldcups_and_championships.csv

- **File:** `ifsc_all_comps_csv_to_json.py`
  - **Description:** Step 3/5 in IFSC scraping
  - **Inputs::** `worldcups_and_championships.csv` 
  - **Outputs:** `worldcups_and_championships.json`

- **File:** `ifsc_comp_scraping.py`
  - **Description:** Step 4/5 in IFSC scraping: Categorizes comps into Wlead, Wboulder,...
  - **Inputs:** 
    - `worldcups_and_championships.json`
  - **Outputs:** `Wlead.json`, `Wboulder.json`, `Wcombined.json`, `Wboulderlead.json`

- **File:** `ifsc_json_to_df.py`
  - **Description:** Step 5/5 in IFSC scraping: Flattens nested json cells into separate columns with single values
  - **Inputs:** 
    - `worldcups_and_championships.json`
  - **Temoporary Outputs:** E.g. `Wlead_initial.csv`, `Wlead_1.csv`
  - **Outputs:** `Wlead.csv`, `Wboulder.csv`, `Wcombined.csv`, `Wboulderlead.csv`


# Note:
The WCombined dataset can be disregarded for our purposes since it simply combines points from lead and boulder from the 2021 Moscow World Championships. 
The detailed lead and boulder results are already recorded in the respective datasets of Wlead and Wboulder.

However, the Lead & Boulder World Championships from Bern 2023 was separate from the Boulder and Lead World Championships respectively. It contains only semifinal and final results since qualifications were determined by __. Hence each competition has distinct results in the Wboulder, Wlead and Wboulderlead datasets and they have been aggregated in the dataset __.

For Wboulder and Wlead, cleaned _3.csv before further normalizing json columns for efficiency