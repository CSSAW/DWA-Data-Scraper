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
    #Returns a dictionary with
    # df:Pandas dataframe with the data from the station
    # lattitude:the lattitude of the station
    # longitude:The longitude of the station 
    # station:The name of the station
    # river: the river that the station is on

    outputDict = {}
    stationInferface = documentDownloader(stationInterfaceURL,alwaysDownload=alwaysDownload, storeData=storeData)
    baseURL = stationInterfaceURL[:stationInterfaceURL.rfind("/")+1]
    outputDict["lat"] = stationInferface.find(id="tbLat").get("value")
    outputDict["long"] = stationInferface.find(id="tbLong").get("value")
    outputDict["station"] = stationInferface.find(id="tbStation").get("value")
    outputDict["river"] = stationInferface.find(id="labPlace").get_text().strip();

    # The construction of the URL below was created by analysing the output of a form
    stationDataURLPrimary = baseURL + "HyData.aspx?Station=" + stationInferface.find(id="tbStation").get("value") +stationInferface.find("input", {"name":"ctl05"}).get("value") \
    + "&DataType=Point&StartDT=" + stationInferface.find("input", {"name":"ctl06"}).get("value") \
    + "&EndDT=" + stationInferface.find("input", {"name":"tbEnd_0"}).get("value") \
    + "&SiteType=" + stationInferface.find("input", {"name":"tbSiteType"}).get("value")

    stationDataPrimary = documentDownloader(stationDataURLPrimary,alwaysDownload=alwaysDownload, storeData=storeData) 
    # Remove any non-table items from the webPage. 
    foundPre = stationDataPrimary.find("pre")
    if foundPre != None:     
        stationDataStrPrimary = foundPre.get_text()
        substrStartKeyword = "Surface Water Level\n"
        stationDataStrPrimary = stationDataStrPrimary[stationDataStrPrimary.find(substrStartKeyword)+len(substrStartKeyword):]

        # Use a stringIo object to use the pandas read_fwf function. 
        # This converts a pure text table with a bunch of columns to a pandas dataframe. 
        strBuffer = io.StringIO(stationDataStrPrimary)
        outputDict["dfPrimary"] = pd.read_fwf(strBuffer)
        strBuffer.close()
    else:
        outputDict["dfPrimary"] = None
    
    # The construction of the URL below was created by analysing the output of a form 
    stationDataURLFlow = baseURL + "HyData.aspx?Station=" + stationInferface.find(id="tbStation").get("value") +stationInferface.find("input", {"name":"ctl05"}).get("value") \
    + "&DataType=Daily&StartDT=" + stationInferface.find("input", {"name":"ctl06"}).get("value") \
    + "&EndDT=" + stationInferface.find("input", {"name":"tbEnd_0"}).get("value") \
    + "&SiteType=" + stationInferface.find("input", {"name":"tbSiteType"}).get("value")

    stationDataFlow = documentDownloader(stationDataURLFlow,alwaysDownload=alwaysDownload, storeData=storeData) 
    # Remove any non-table items from the webPage. 
    foundPre = stationDataFlow.find("pre")
    if foundPre != None:       
        stationDataStrFlow = foundPre.get_text()
        substrStartKeyword = "DATE     D AVG F/R  QUAL"
        stationDataStrFlow = stationDataStrFlow[stationDataStrFlow.find(substrStartKeyword):]

        # Use a stringIo object to use the pandas read_fwf function. 
        # This converts a pure text table with a bunch of columns to a pandas dataframe. 
        strBuffer = io.StringIO(stationDataStrFlow)
        outputDict["dfFlow"] = pd.read_fwf(strBuffer)
        strBuffer.close()
    else:
        outputDict["dfFlow"] = None

    return outputDict#{"dfPrimary": stationDataPrimaryDf, "dfFlow":stationDataFlowDf, "lat": lattitude, "long":longitude,"station":stationName}