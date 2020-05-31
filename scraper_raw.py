import argparse
import scraper_functions

parser = argparse.ArgumentParser(description="Scrape data from the South African department of water and sanitation.")
parser.add_argument("--station_list_url", default="http://www.dwa.gov.za/Hydrology/Verified/HyStations.aspx?Region=A&StationType=rbRiver", help="The url to the list of the stations. Defaults to the verified list for the Limpopo basin.")
parser.add_argument("--always_download", action='store_true', help="Will download webpages regardless if they are already downloaded. This is akin to refreshing a page in a web browser")
parser.add_argument("--store_web_data", action='store_true', help="Will store web data so that the script doesn't have to redownload everything. This is usefull for debugging because the script will run much quicker.")
args = parser.parse_args()

stationListSoup = scraper_functions.documentDownloader(args.station_list_url, alwaysDownload=args.always_download, storeData=args.store_web_data)
stationListTable = stationListSoup.find(id="tableStations")
if stationListTable == None:
    raise ValueError("The table with the id tableStations has not been found.")

dataURL = args.station_list_url[:args.station_list_url.rfind("/")+1]
stationListLinks = [i.get("href") for i in stationListTable.find_all('a')]

stationInferface = scraper_functions.documentDownloader(dataURL+stationListLinks[0],alwaysDownload=args.always_download, storeData=args.store_web_data)
stationDataURL = dataURL + "HyData.aspx?Station=" + stationInferface.find(id="tbStation").get("value") +stationInferface.find("input", {"name":"ctl05"}).get("value") \
    + "&DataType=Point&StartDT=" + stationInferface.find("input", {"name":"ctl06"}).get("value") \
    + "&EndDT=" + stationInferface.find("input", {"name":"tbEnd_0"}).get("value") \
    + "&SiteType=" + stationInferface.find("input", {"name":"tbSiteType"}).get("value") 
print(stationDataURL)