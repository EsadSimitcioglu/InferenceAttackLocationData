import pandas as pd
import numpy as np
import json
from matplotlib import pyplot as plt
from requests import delete
from shapely import geometry

max_lat =  -8.58     ##-8.28    ### 52.900803
max_long = 41.18   ### 51.037119
min_lat =  -8.68         ##-8.78    ### -9.781308
min_long = 41.14   ### 31.992111

def preprocess_kaggle():
    data = pd.read_csv("dataset/kaggle-taxi-data.csv",
                    chunksize=10000,
                    usecols=['POLYLINE', 'TIMESTAMP'],
                    converters={'POLYLINE': lambda x: json.loads(x) })
    with open("dataset/kaggle.csv", 'w') as f:
        f.write("timestamp,lat,lon\n")


    latIntrDict = {}
    longIntrDict = {}
    interval = 0.002
    for num in np.arange(min_lat,max_lat,interval):
        #print(num)
        latIntrDict[str(num)+'/'+str(num + interval)] = 0

    for num in np.arange(min_long,max_long,interval):
        #print(num)
        longIntrDict[str(num)+'/'+str(num + interval)] = 0
    #print(latIntrDict)
    #user_mat = []
    lats = []
    longs = []
    lat_outliers = 0
    long_outliers = 0
    for i, chunk in enumerate(data):
        for path in chunk.POLYLINE:
            if len(path) > 0:  ##0 lat 1 long
                # for cor in path:     
                #     if cor[0]<-8 and cor[0]>-9:  ##to eliminate outliers  ## -6 and -10
                #         lats.append(cor[0])
                #     else:
                #         lat_outliers += 1
                #     if cor[1]<42 and cor[1]>41:  ## 42 and 40
                #         longs.append(cor[1])
                #     else:
                #         long_outliers += 1
                for cor in path:
                    # for key in latIntrDict.keys():
                    #     nums = key.split('/')
                    #     nums = [float(i) for i in nums]
                    #     if nums[0] <= cor[0] and nums[1] >= cor[0]:
                    #         latIntrDict[key] += 1

                    for key in longIntrDict.keys():
                        nums = key.split('/')
                        nums = [float(i) for i in nums]
                        if nums[0] <= cor[1] and nums[1] >= cor[1]:
                            longIntrDict[key] += 1
        if i % 10 == 0:
            print("Chunk", i, "done.")
    
    #print(lats)
    #print("*****************************************************************")
    #print(longs)
    #print("*****************************************************************")
    #plt.hist(lats,bins = 10)
    #plt.show()
    print(latIntrDict)
    print(longIntrDict)
    latsObj = json.dumps(latIntrDict)
    jsonFile = open("latsdict.json","w")
    jsonFile.write(latsObj)
    jsonFile.close()

    longsObj = json.dumps(longIntrDict)
    jsonFile = open("longsdict.json","w")
    jsonFile.write(longsObj)
    jsonFile.close()

    print("Max lats:")
    print(max(lats))
    print("Max longs:")
    print(max(longs))
    print("Min lats:")
    print(min(lats))
    print("Min longs:")
    print(min(longs))

    print(lat_outliers/len(lats))
    print(long_outliers/len(longs))
    # latsObj = json.dumps(lats)
    # jsonFile = open("lats.json","w")
    # jsonFile.write(latsObj)
    # jsonFile.close()

    # delete(latsObj)
    # delete(lats)


    # longsObj = json.dumps(longs)
    # jsonFile = open("longs.json","w")
    # jsonFile.write(longsObj)
    # jsonFile.close()
    # #print(user_mat)



def create_path_list(chunk):
    res = []
    for path in chunk.POLYLINE:
        print(path)
        print("******************************************************")
        if len(path) > 0:
            #res.append(path[0][::-1])
            res.append(path)
        else:
            res.append([float("NaN"), float("NaN")])
    return res


preprocess_kaggle()