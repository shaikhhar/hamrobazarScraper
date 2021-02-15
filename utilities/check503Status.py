from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime


def isSiteDown(soup):
    if "Temporarily Not Available 503" in str(soup.find('title').text):
        return True
    else:
        return False
