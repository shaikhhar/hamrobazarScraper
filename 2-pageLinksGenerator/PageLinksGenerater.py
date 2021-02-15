import pandas as pd
import numpy as np
import json
import os

with open('1-categoryCrawler/categories.json', 'r') as f:
    categoryDataList = json.load(f)


def getlistPageLinks(url, numberOfPages, catId):
    
    listPageLinks = []
    for pageNo in range(0, int(numberOfPages)):
        pageSuffix = "?catid={}&order=siteid&offset={}".format(
            catId, pageNo*20)
        pageLink = url+pageSuffix
        listPageLinks.append(pageLink)
    return listPageLinks

def getAllPageLinks():
    pageLinkList = []
    pageIndex = 0
    for categoryData in categoryDataList:
        categoryPageLinks = getlistPageLinks(
            categoryData['categoryUrl'], categoryData['numberOfPages'], categoryData['catId'])
        for categoryPageLink in categoryPageLinks:
            pageLinkList.append(
                {'pageIndex': pageIndex, 'pageLink': categoryPageLink, 'hasCrawled': 0})
            pageIndex += 1
    return pageLinkList

def savePageLinksJSON():
    allPageLinks = getAllPageLinks()
    with open('2-pageLinksGenerator/pageLinks.json', 'w') as fp:
            json.dump(allPageLinks, fp)
    print("pageLinks.json generated")
    print("Total number of pages: "+str(len(allPageLinks)))


if os.path.exists('2-pageLinksGenerator/pageLinks.json'):
    option = input(
        "PageLinks.json already exists. Press any key to cancel or press R to reset pageLinks.json").lower()
    if option == 'r':
        savePageLinksJSON()
else:
    savePageLinksJSON()
