import os
import pandas as pd
import json
from sklearn.preprocessing import StandardScaler


primaryDf = pd.DataFrame(columns=['DATE', 'TIME', 'COR.LEVEL', 'QUA', 'COR.FLOW', 'QUA.1','lat','long','river','station'])
readDf = pd.read_csv("csv_output/A2H001_PRIMARY.csv",header = 1)


# jsonDataFile = open("csv_output/A2H001_PRIMARY.csv",'r')
# jsonData = jsonDataFile.readline()[1:]
# jsonData = json.loads(jsonData)
# jsonDataFile.close()
# readDf["station"] = "A2H001"
# readDf["lat"] = jsonData["lat"]
# readDf["long"] = jsonData["long"]
# readDf["river"] = jsonData["river"]
# primaryDf = primaryDf.append(readDf)
print(primaryDf)

for i in os.listdir("csv_output/"):
    if i.endswith("PRIMARY.csv"):
        jsonDataFile = open(os.path.join("csv_output", i),'r')
        jsonData = jsonDataFile.readline()[1:]
        jsonData = json.loads(jsonData)
        jsonDataFile.close()
        readDf = pd.read_csv(os.path.join("csv_output",i),header = 1)
        readDf["station"] = i.split("_")[0]
        readDf["lat"] = jsonData["lat"]
        readDf["long"] = jsonData["long"]
        readDf["river"] = jsonData["river"][:32]
        primaryDf = primaryDf.append(readDf)
    # elif i.endswith("FLOW.csv"):

primaryDf.to_csv("total_primary.csv", index=False)
primaryDfPreprocessed = primaryDf.dropna() 
print(primaryDfPreprocessed[primaryDfPreprocessed['COR.FLOW'] > 1])

primaryDfPreprocessed[['COR.LEVEL','COR.FLOW']].head()
primaryDfPreprocessed[['COR.LEVEL','COR.FLOW']] = StandardScaler(copy=False).fit_transform(primaryDfPreprocessed[['COR.LEVEL','COR.FLOW']])
primaryDfPreprocessed.to_csv("total_primary_preprocessed.csv")
print(primaryDfPreprocessed[primaryDfPreprocessed['COR.LEVEL'] > 1])
print(primaryDfPreprocessed[primaryDfPreprocessed['COR.FLOW'] > 1])