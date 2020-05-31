from bs4 import BeautifulSoup
import os
import urllib
import pickle


def documentDownloader(urlString, alwaysDownload=False, storeData=True,  dataPath="raw_data/"):
    # Returns the soup for a particular document. It will also store the file in the /raw_data directory
    documentPath = dataPath + urlString.replace("/", "|")
    soup = None

    if not os.path.exists(dataPath):
        os.mkdir(dataPath)

    if alwaysDownload or not os.path.exists(documentPath):
        print("Downloading data")
        html = urllib.request.urlopen(urlString)
        soup = BeautifulSoup(html, "html.parser")
        print("Data downloaded")
        if storeData:
            dataFile = open(documentPath, "wb")
            pickle.dump(soup, dataFile)
            dataFile.close()
    else:
        print("Data already stored, obtaining")
        dataFile = open(documentPath, "rb")
        soup = pickle.load(dataFile)
        dataFile.close()

    return soup
