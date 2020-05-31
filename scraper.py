import argparse
import scraper_functions
import pandas as pd
import os


parser = argparse.ArgumentParser(description="Scrape data from the South African department of water and sanitation.")
parser.add_argument("--station_list_url", default="http://www.dwa.gov.za/Hydrology/Verified/HyStations.aspx?Region=A&StationType=rbRiver", help="The url to the list of the stations. Defaults to the verified list for the Limpopo basin.")
parser.add_argument("--data_output_dir", default="csv_output", help="This is where the CSVs of data from each of the stations will go.")
parser.add_argument("--always_download", action='store_true', help="Will download webpages regardless if they are already downloaded. This is akin to refreshing a page in a web browser")
parser.add_argument("--store_web_data", action='store_true', help="Will store web data so that the script doesn't have to redownload everything. This is usefull for debugging because the script will run much quicker.")
args = parser.parse_args()

stationListSoup = scraper_functions.documentDownloader(args.station_list_url, alwaysDownload=args.always_download, storeData=args.store_web_data)
stationListTable = stationListSoup.find(id="tableStations")
if stationListTable == None:
    raise ValueError("The table with the id tableStations has not been found.")

baseURL = args.station_list_url[:args.station_list_url.rfind("/")+1]
stationListLinks = [i.get("href") for i in stationListTable.find_all('a')]

if not os.path.exists(args.data_output_dir):
    os.mkdir(args.data_output_dir)

for stationLink in stationListLinks:
    stationData = scraper_functions.getStationData(baseURL+stationLink,alwaysDownload=args.always_download, storeData=args.store_web_data)
    csvPath = os.path.join(args.data_output_dir,stationData["station"]+".csv")
    stationData["df"].to_csv(csvPath,sep=",")
    metadataStr = "#" + (str)({"lat":stationData["lat"],"long":stationData["long"]}) + "\n"
    csvFile = open(csvPath, "r+")
    csvContent = csvFile.read()
    csvFile.seek(0)
    csvFile.write(metadataStr)
    csvFile.write(csvContent)
    csvFile.close()