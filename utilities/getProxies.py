import requests

proxies1 = requests.get(
    'http://filefab.com/api.php?l=L_KWQQ-IJjsDxbnOBTxQ8GIIVmI1t1HWvhjS8mXut74')

proxies2 = requests.get(
    'http://list.didsoft.com/get?email=skrbasnet@gmail.com&pass=iyf4b5&pid=http3000&https=yes&showcountry=no&country=NP')


def proxiesList(proxyRequest):
    proxyIPlist = proxyRequest.text.splitlines()
    proxyList = []
    for proxyIP in proxyIPlist:
        proxy = {"https": proxyIP}
        proxyList.append(proxy)
    return proxyList


proxyList = proxiesList(proxies2)
for proxy in proxiesList(proxies1):
    proxyList.append(proxy)

# print(len(proxyList))
