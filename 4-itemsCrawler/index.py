from pathlib import Path
import os
import pandas as pd
import json
from ItemFieldsCrawler import parse
import time
import sys

jsonFileCount = 14


def createJsonFile(name):
    if not os.path.exists('4-itemsCrawler/json-parts/'+name):
        open('4-itemsCrawler/json-parts/'+name, 'w')
    else:
        pass


def jsonFileInfo(fileNumber):
    startIndex = (fileNumber-1)*10000
    endIndex = fileNumber*10000-1 if fileNumber * \
        10000 <= len(itemLinks) else len(itemLinks) - 1
    total = 10000 if fileNumber * \
        10000 <= len(itemLinks) else endIndex - startIndex + 1
    crawled = 0
    for itemLink in itemLinks:
        if itemLink['linkIndex'] >= startIndex and itemLink['linkIndex'] <= endIndex and itemLink['hasCrawled'] == 1:
            crawled += 1
    return {'fileName': str(fileNumber)+'.json', 'start': startIndex, 'end': endIndex, 'crawled': crawled, 'remaining': total-crawled, 'total': total}


# As of Nov 2020, there were 1.45 lack items
# 1 file = 10,000 items
# To fill 1.45 lack items, we need 15 json files

# Creating 15 json files
for i in range(1, jsonFileCount):
    createJsonFile(str(i)+'.json')

pathToItemLinks = str(Path(__file__).parent.parent) + \
    "/3-itemLinksCrawler/itemLinks.json"
# print(pathToItemLinks)

itemLinks = json.load(open(pathToItemLinks, 'r'))

dfInfo = pd.DataFrame(
    columns=['fileName', 'start', 'end', 'crawled', 'remaining', 'total'])

for i in range(1, jsonFileCount):
    dfInfo = dfInfo.append(jsonFileInfo(i), sort=False, ignore_index=True)
print(dfInfo)

option = input(
    "Enter fileName to begin crawling those indexes (Eg: 1.json) \n")

while option not in dfInfo['fileName'].to_list():
    print("{} is invalid. ".format(option))
    option = input("\nEnter valid fileName \n")

start = dfInfo.loc[dfInfo.fileName == option].start.values[0]
end = dfInfo.loc[dfInfo.fileName == option].end.values[0]
filename = dfInfo.loc[dfInfo.fileName == option].fileName.values[0]
total = dfInfo.loc[dfInfo.fileName == option].total.values[0]

if os.path.getsize('4-itemsCrawler/json-parts/'+filename) == 0:
    parsedItemList = []
else:
    parsedItemList = json.load(
        open('4-itemsCrawler/json-parts/'+filename, 'r'))
# print(parsedItemList)
itemCrawled = dfInfo.loc[dfInfo.fileName == option].crawled.values[0]
crawledNow = 0
for itemLink in itemLinks:
    if itemLink['linkIndex'] >= start and itemLink['linkIndex'] <= end:
        if itemLink['hasCrawled'] == 0:
            parsedInfo = parse(itemLink['itemLink'])
            parsedItemList.append(parsedInfo)
            json.dump(parsedItemList, open('4-itemsCrawler/json-parts/'+filename, 'w'),
                      sort_keys=True)  # update the json file
            # mark itemLinks.json 's item as crawled
            itemLink['hasCrawled'] = 1
            json.dump(itemLinks, open(pathToItemLinks, 'w'), sort_keys=True)
            crawledNow += 1
            itemCrawled += 1
            sys.stdout.write('\r')
            sys.stdout.write("Crawled: %d / %d" % (itemCrawled, total))
            if crawledNow % 20 == 0:
                time.sleep(30)
