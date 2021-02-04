import requests
import re
import json
import datetime
import time

user_re=re.compile(r"loggedUser\":\"([A-Za-z0-9]+)\"")
date_re=re.compile(r"lastSync\":\"([0-9-]+) ")
gse_re=re.compile(r"gsechash=\"([a-z0-9]+)\"")
token_re=re.compile(r"name=\"csrfauth\" value=\"([a-z0-9]*)\">")

times=[]

with open("settings.json","r") as c:
    f = c.read()
    jes=json.loads(f)
    username=jes["Login"]["username"]
    password=jes["Login"]["password"]
    edupageurl=jes["School"]["edupageurl"]
    zoompath=jes["Zoom"]["path"]
    for x in jes["School"]["starts"]:
        times.append(x)

def hod():
    while True:
        time.sleep(30)
        current_time = datetime.datetime.now()
        timee=f"{str(current_time.hour)}:{current_time.minute}"
        count=0
        for x in times:
            if x == timee:
                return login(count+2)
            count += 1
      
def login(hour):
    try:
        with requests.Session() as c:
            tokenreq=c.get(edupageurl)
            csrf=token_re.findall(tokenreq.text)
            data={"csrfauth":csrf[0],"username":username,"password":password}
            loginreq=c.post(edupageurl+"/login/edubarLogin.php",data=data)
            classreq=c.get(edupageurl+"/dashboard/eb.php")
            user=user_re.findall(classreq.text)
            text=classreq.text
            out=text.split('classbook.fill("'+user[0]+'", ')[1]
            out2=out.split(", []);gi")[0]
            gse=gse_re.findall(classreq.text)
            date=date_re.findall(classreq.text)
            jesko=json.loads(out2)
            link=jesko['dates'][date[0]]['plan'][hour]['ol_url']
            subid=jesko['dates'][date[0]]['plan'][hour]['subjectid']
            headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
            'Content-type':'application/json; charset=UTF-8',
            'Accept':'*/*',
            'Origin':edupageurl,
            'Sec-Fetch-Site':'same-origin',
            'Sec-Fetch-Mode':'cors',
            'Sec-Fetch-Dest':'empty',
            'Referer':edupageurl+'/dashboard/eb.php',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'en-US,en;q=0.9',
            }
            data={"__args":[None,{"date":date[0],"ol_url":link,"subjectid":subid,"click":True}],"__gsh":gse[0]}
            join=c.post(edupageurl+"/dashboard/server/onlinelesson.js?__func=getOnlineLessonOpenUrl",json=data,headers=headers)
            print(join.text)
            return hod()
    except Exception as exc:
        print("Trying again.")
        return hod()
if __name__ == "__main__":
    hod()