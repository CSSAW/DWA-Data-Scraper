from bs4 import BeautifulSoup
import argparse

parser = argparse.ArgumentParser(description="Scrape data from the South African department of water and sanitation.")
parser.add_argument("--station_list_url", help="The url to the list of the stations. Defaults to the verified list for the Limpopo basin.", default="http://www.dwa.gov.za/Hydrology/Verified/HyStations.aspx?Region=A&StationType=rbRiver")
args = parser.parse_args() 
