from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import json
from utilities.getSourceText import getSourceText


def getCategoryData(url):
    soupURL = getSourceText(url)
    soupTable = soupURL.find('table', id="tab_cat")
    soupTableTD = soupTable.find_all(
        'font', attrs={"size": "2", "face": "Arial, Helvetica, sans-serif"}
    )
    categoryCount = 0
    categoryDF = pd.DataFrame(
        columns=['catId', 'categoryUrl', 'outputFileName', 'numberOfItems', 'numberOfPages'])
    for soupTD in soupTableTD:
        aElement = soupTD.find('a')
        linkCategory = str(url+aElement['href'])
        noItemsInsideBracket = soupTD.find('small').text.strip()  # no of Items inside bracket
        noItems = int(noItemsInsideBracket[1:-1])  # brackets removed
        outputFileName = aElement['href']+".json"
        soupCategory = getSourceText(linkCategory)
        try:
            catId = int(soupCategory.find('input', attrs={
                "type": "hidden", "name": "catid"
            }
            )['value'])
        except:
            catId = ''
        df_temp = pd.DataFrame(
            {
                'catId': [catId],
                'categoryUrl': [linkCategory],
                'outputFileName': [outputFileName],
                'numberOfItems': [noItems],
                'numberOfPages': [noItems/20 if noItems % 20 == 0 else noItems//20+1]
            }, index=[categoryCount])
        categoryDF = categoryDF.append(df_temp, sort=False)
        categoryCount += 1
    return categoryDF

# run this to persist category info to .json file, to be refreshed by running RefreshcategoryDFJsonFile.py script


def saveCategoryDataToFile():
    categoryDF = getCategoryData('https://hamrobazaar.com/')
    print(categoryDF)
    with open('1-categoryCrawler/categories.json', 'w') as fp:
        json.dump(categoryDF.to_dict(orient="records"), fp)


saveCategoryDataToFile()

