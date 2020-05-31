from bs4 import BeautifulSoup
import os
import urllib
import pickle
import requests
import sys
import pandas as pd
import io

#Necessary for pickle on soup objects
sys.setrecursionlimit(100000)
def documentDownloader(urlString, alwaysDownload=False, storeData=False,  dataPath="raw_data"):
    # Returns the soup for a particular document. It will also store the file in the /raw_data directory
    documentPath = os.path.join(dataPath,urlString.replace("/", "|"))
    soup = None

    if not os.path.exists(dataPath):
        os.mkdir(dataPath)

    if alwaysDownload or not os.path.exists(documentPath):
        print("Downloading data from",urlString)
        html = urllib.request.urlopen(urlString)
        soup = BeautifulSoup(html, "html.parser")
        print("Data downloaded")
        if storeData:
            dataFile = open(documentPath, "wb")
            pickle.dump(soup, dataFile)
            dataFile.close()
    else:
        print("Data already stored, obtaining. URL:", urlString)
        dataFile = open(documentPath, "rb")
        soup = pickle.load(dataFile)
        dataFile.close()

    return soup

def getStationData(stationInterfaceURL, alwaysDownload=False, storeData=False,  dataPath="raw_data"):
    #Returns a Pandas dataframe with the data from the station
    stationInferface = documentDownloader(stationInterfaceURL,alwaysDownload=alwaysDownload, storeData=storeData)
    baseURL = stationInterfaceURL[:stationInterfaceURL.rfind("/")+1]

    # The construction of the URL below was created by analysing the output of a 
    stationDataURL = baseURL + "HyData.aspx?Station=" + stationInferface.find(id="tbStation").get("value") +stationInferface.find("input", {"name":"ctl05"}).get("value") \
    + "&DataType=Point&StartDT=" + stationInferface.find("input", {"name":"ctl06"}).get("value") \
    + "&EndDT=" + stationInferface.find("input", {"name":"tbEnd_0"}).get("value") \
    + "&SiteType=" + stationInferface.find("input", {"name":"tbSiteType"}).get("value")

    stationData = documentDownloader(stationDataURL,alwaysDownload=alwaysDownload, storeData=storeData) 
    # Remove any non-table items from the webPage. 
    stationDataStr = stationData.find("pre").get_text()
    substrStartKeyword = "Surface Water Level\n"
    stationDataStr = stationDataStr[stationDataStr.find(substrStartKeyword)+len(substrStartKeyword):]

    # Use a stringIo object to use the pandas read_fwf function. 
    # This converts a pure text table with a bunch of columns to a pandas dataframe. 
    strBuffer = io.StringIO(stationDataStr)
    stationDataDf = pd.read_fwf(strBuffer)
    strBuffer.close()
    return stationDataDf