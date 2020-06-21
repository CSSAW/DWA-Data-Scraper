# DWA-Data-Scraper
Scrape hydrological data from the South African department of Water and Sanitation for use in modeling.

The source of the data can be found at this address, http://www.dwa.gov.za/Hydrology/Verified/hymain.aspx

This project should first download the raw files from each of the stations and then convert them to CSVs for easier use. The CSVs will have a heading with a commented out json string containing some metadata.
<br/>
<br/>
Example:
<br/>
#{'lat': '-22.49135', 'long': '29.98309', 'river': 'Sand River @ Dorothy'}


```
usage: scraper.py [-h] [--station_list_url STATION_LIST_URL]
                  [--data_output_dir DATA_OUTPUT_DIR] [--always_download]
                  [--store_web_data]

Scrape data from the South African department of water and sanitation.

optional arguments:
  -h, --help            show this help message and exit
  --station_list_url STATION_LIST_URL
                        The url to the list of the stations. Defaults to the
                        verified list for the Limpopo basin.
  --data_output_dir DATA_OUTPUT_DIR
                        This is where the CSVs of data from each of the
                        stations will go.
  --always_download     Will download webpages regardless if they are already
                        downloaded. This is akin to refreshing a page in a web
                        browser
  --store_web_data      Will store web data so that the script doesn't have to
                        redownload everything. This is usefull for debugging
                        because the script will run much quicker.
```
