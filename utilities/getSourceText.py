from bs4 import BeautifulSoup
import requests
import cloudscraper
import time
from utilities.check503Status import isSiteDown

# set user agents
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}

scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance
# Or: scraper = cloudscraper.CloudScraper()  # CloudScraper inherits from requests.Session


def getSourceText(url):
    source = scraper.get(url, headers=headers).text
    soup = BeautifulSoup(source, 'lxml')
    interruptCount = 1
    while isSiteDown(soup):
        print("Interruption #{} Site down: waiting ...".format(interruptCount))
        time.sleep(1*60)  # wait till the site is back up
        source = scraper.get(url, headers=headers).text
        soup = BeautifulSoup(source, 'lxml')
        interruptCount += 1

    return soup


# print(getSourceText('https://hamrobazaar.com/'))
