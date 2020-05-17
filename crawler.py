from bs4 import BeautifulSoup
import requests
import json
import re

headers = {'User-Agent': 'Mozilla/5.0'}

url = 'https://hamrobazaar.com/'

source = requests.get('https://hamrobazaar.com/c6-apparels-and-accessories', headers=headers).text
soup = BeautifulSoup(source, 'lxml')
tds= soup.find_all('td')

product_link_set= set()

dictSellerPhone = []

for td in tds:
    # find all links that has target="_blank" and save it to a set
    links = soup.find_all('a', href=True, attrs={"target": "_blank"})
    for a in links:
        # print(a['href'])
        # print('\n')
        product_link_set.add(url+str(a['href']))
        
for a in product_link_set:
    # print(a)
    sourceProduct= requests.get(a, headers=headers).text
    soupProduct= BeautifulSoup(sourceProduct, 'lxml')
    soldBy= str(soupProduct.find('td', attrs={"id": "white", "valign": "bottom", "width" : "75%"}).text).splitlines()[0].strip()
    phoneText =  re.findall("Mobile Phone:.*[0-9]{10}" ,str(soupProduct))
    if (phoneText):
        phone= str(phoneText[0]).split()[-1]
    else:
        phone = ''

    dictSellerPhone.append({'name':soldBy, 'phone': phone})
    print(soldBy)
    print(phone)

print(dictSellerPhone)