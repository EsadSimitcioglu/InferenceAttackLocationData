import pandas as pd
import numpy as np
import json
from matplotlib import pyplot as plt
import heapq


jsonFile = open("latsdict.json","r")
latIntrDict = json.load(jsonFile)

jsonFile = open("longsdict.json","r")
longIntrDict = json.load(jsonFile)

print(heapq.nlargest(8,latIntrDict.values()))
largestLats = heapq.nlargest(8,latIntrDict.values())

newlatIntrDict = {}
for key in latIntrDict:
    if latIntrDict[key] in largestLats:
        vals = key.split('/')
        vals = [float("{:.2f}".format(float(i))) for i in vals]
        newKey = str(vals[0])+'/'+str(vals[1])
        newlatIntrDict[newKey] = latIntrDict[key]

#print(newlatIntrDict)

y_pos = range(len(newlatIntrDict.keys()))
plt.bar(y_pos, newlatIntrDict.values(), color='g')
plt.xticks(y_pos, newlatIntrDict.keys(), rotation=90)
plt.show()

## for longtitude
print(heapq.nlargest(11,longIntrDict.values()))
largestLongs = heapq.nlargest(20,longIntrDict.values()) ##was 11
newlongIntrDict = {}
for key in longIntrDict:
    if longIntrDict[key] in largestLongs:
        vals = key.split('/')
        vals = [float("{:.4f}".format(float(i))) for i in vals]
        newKey = str(vals[0])+'/'+str(vals[1])
        newlongIntrDict[newKey] = longIntrDict[key]

y_pos = range(len(newlongIntrDict.keys()))
plt.bar(y_pos, newlongIntrDict.values(), color='g')
plt.xticks(y_pos, newlongIntrDict.keys(), rotation=90)
plt.show()