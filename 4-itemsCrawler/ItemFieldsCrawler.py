from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime
from utilities.check503Status import isSiteDown
import time
from utilities.getSourceText import getSourceText


def parse(url):
    soupProduct = getSourceText(url)
    try:
        itemName = str(soupProduct.find(
            'font', attrs={"size": "3", "face": "Verdana"}).text).strip()
    except:
        itemName = ''

    try:
        soldBy = str(soupProduct.find('td', attrs={
                     "id": "white", "valign": "bottom", "width": "75%"}).text).splitlines()[0].strip()
    except:
        soldBy = ''

    try:
        phoneText = re.findall("Mobile Phone:.*[0-9]{10}", str(soupProduct))
        phone = str(phoneText[0]).split()[-1]
    except:
        phone = ''

    try:
        AdPostDate = re.search(
            "Ad Post Date:[\s\S]{0,50}\d{2}-\d{2}-\d{4}", str(soupProduct)).group().split()[-1]
        date = datetime.strftime(datetime.strptime(
            AdPostDate, '%d-%m-%Y').date(), '%Y/%m/%d')
    except:
        date = ''
    # print(date)195

    try:
        cat = str(soupProduct.find_all('u')[1].text)
    except:
        cat = ''
    try:
        subcat = str(soupProduct.find_all('u')[2].text)
    except:
        subcat = ''

    try:
        locationRaw = re.search(
            "Location:[\s\S]{0,100}</td></tr>", str(soupProduct)).group()
        # from locationRaw, slice between td tag, then replace any <br>s with " ", then get rid of whitespace, then get the last string
        locationDetail = str(locationRaw[locationRaw.find("white\">")+len("white\">"):locationRaw.find("</td></tr>")]
                             ).replace("<br>", ", ").replace("<br/>", ", ").replace("</br>", ", ").strip()[:-1]
        location = locationDetail.split(" ")[-1]
    except:
        locationDetail = ''
        location = ''

    try:
        price = int(str(soupProduct.find('font', class_="bigprice").text).replace(
            "Rs. ", "").replace(",", "").strip())
    except:
        price = ''

    try:
        sellerId = re.search("siteid=\d{2,8}", str(
            soupProduct)).group().split(sep="=")[-1]
    except:
        sellerId = ''

    try:
        conditionRaw = re.search(
            "Condition:[\s\S]{10,100}</tr>", str(soupProduct)).group()
        condition = conditionRaw[conditionRaw.find(
            "75%\">")+len("75%\">"):conditionRaw.find("</td></tr")]
    except:
        condition = ''

    try:
        pictureUrl = soupProduct.find('img', id="inimg").get(
            "src").replace("_large", "")
    except:
        pictureUrl = ''

    try:
        description = soupProduct.find('td', attrs={"valign": "top", "bgcolor": "#C6C6D9", "align": "left"}).parent.next_sibling.findChildren(
            'td', recursive=False)[0].text.replace("\r", " ").replace("\n", " ").replace("<br>", " ").replace("\t", " ").strip()
    except:
        description = ''
        # add seller name and phone to the listSellerPhone list
    return {'itemName': itemName, 'sellerName': soldBy, 'category': cat, 'subCategory': subcat, 'phone': phone, 'date': date, 'location': location, 'locationDetail': locationDetail, 'price': price, 'sellerId': sellerId, 'condition': condition, 'pictureUrl': pictureUrl, 'description': description, 'url': url}


# url = "https://hamrobazaar.com/i1927899-puja-kapur-powder-200gm-camphor-powder.html"

# print(parse(url))
