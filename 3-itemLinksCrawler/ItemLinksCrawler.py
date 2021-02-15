from bs4 import BeautifulSoup
import time
from utilities.getSourceText import getSourceText
import json
from pathlib import Path
import os
import pandas as pd
import sys

pathToPageLinks = str(Path(__file__).parent.parent) + \
    "/2-pageLinksGenerator/pageLinks.json"


def getItemLinksFromPage(url):
    base_url = 'https://hamrobazaar.com/'
    soupItem = getSourceText(url)
    tds = soupItem.find_all('td')

    # initialize set of links to product page
    item_urls = set()

    for td in tds:
        # find all links that has target="_blank" which is the links to product page and save it to a set
        links = soupItem.find_all('a', href=True, attrs={"target": "_blank"})
        for a in links:
            item_urls.add(base_url+str(a['href']))
    return item_urls

def showItemLinksCrawlingInfo():
    with open(pathToPageLinks, 'r') as fp:
        pageLinks = json.load(fp)
    pageCrawled = 0
    for link in pageLinks:
        if link['hasCrawled'] == 1:
            pageCrawled += 1
    Remaining = len(pageLinks) - pageCrawled
    dfInfo = pd.DataFrame(
        [{'Total': len(pageLinks), 'Crawled': pageCrawled, 'Remaining': Remaining}], index=[0])
    print(dfInfo)

def crawlItemLinksFromPage(itemLinksOld, lenItemLinksOld):
    with open(pathToPageLinks, 'r') as fp:
        pageLinks = json.load(fp)
    crawlSleeper = 0
    for pageLink in pageLinks:
        if pageLink['hasCrawled'] == 0:
            itemLinksList = getItemLinksFromPage(pageLink['pageLink'])
            pageLink['hasCrawled'] = 1  # flag as crawled
            json.dump(pageLinks, open(pathToPageLinks, 'w'))

            for itemlink in itemLinksList:
                itemLinksOld.append(
                    {'hasCrawled': 0, 'linkIndex': lenItemLinksOld, 'itemLink': itemlink})
                lenItemLinksOld += 1

            json.dump(itemLinksOld, open(
                '3-itemLinksCrawler/itemLinks.json', 'w'), sort_keys=True)

            sys.stdout.write('\r')
            sys.stdout.write("Pages Crawled: %s / %d" %
                             (pageLink['pageIndex']+1, len(pageLinks)))
            crawlSleeper += 1
            if crawlSleeper % 20 == 0:  # if crawled 20 pages then
                time.sleep(30)  # wait 30 seconds before crawling next page

if not os.path.exists(pathToPageLinks):
    print("pageLinks.json file doesn't exist. Run PageLinksGeneratory.py ")
else:
    showItemLinksCrawlingInfo() 

    # crawl link
    if os.path.exists('3-itemLinksCrawler/itemLinks.json'):
        with open('3-itemLinksCrawler/itemLinks.json', 'r') as fpItemLinks:
            itemLinksOld = json.load(fpItemLinks)
            lenItemLinksOld = len(itemLinksOld)
    else:
        itemLinksOld = []
        lenItemLinksOld = 0

    crawlItemLinksFromPage(itemLinksOld, lenItemLinksOld)

