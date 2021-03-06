from bs4 import BeautifulSoup
import requests
import json
import re

# set user agents
headers = {'User-Agent': 'Mozilla/5.0'}

# base url
url = 'https://hamrobazaar.com/'

source = requests.get('https://hamrobazaar.com/c6-apparels-and-accessories', headers=headers).text
soup = BeautifulSoup(source, 'lxml')
tds= soup.find_all('td')

# initialize set of links to product page
product_link_set= set()

# initialize a list to store seller name and phone
listSellerPhone = []

for td in tds:
    # find all links that has target="_blank" which is the links to product page and save it to a set
    links = soup.find_all('a', href=True, attrs={"target": "_blank"})
    for a in links:
        # print(a['href'])
        # print('\n')
        product_link_set.add(url+str(a['href']))
        
for a in product_link_set:
    # print(a)
    sourceProduct= requests.get(a, headers=headers).text
    soupProduct= BeautifulSoup(sourceProduct, 'html.parser')
    soldBy= str(soupProduct.find('td', attrs={"id": "white", "valign": "bottom", "width" : "75%"}).text).splitlines()[0].strip()
    phoneText =  re.findall("Mobile Phone:.*[0-9]{10}" ,str(soupProduct))
    if (phoneText):
        # last substring of phoneText is the phone number, if phone as an empty string
        phone= str(phoneText[0]).split()[-1]
    else:
        phone = ''

    # add seller name and phone to the listSellerPhone list
    listSellerPhone.append({'name':soldBy, 'phone': phone})
    print(soldBy)
    print(phone)
# print the list of object
print(listSellerPhone)