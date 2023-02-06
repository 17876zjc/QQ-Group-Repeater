
import json

import time

from requests_html import HTMLSession

import base64
import datetime
import wglive
import random


url = "https://mjv.jp/0/wg/0.js"

def getChar(i:int)->str:
    if i <= 9:
        return str(i)
    else:
        return str(chr(97-10+i))

def getTag() -> str:
    res = ""
    for i in range(4):
        res += getChar(random.randint(0,35))
    return res

class WgScheduler():
    #wgClient : list[wglive.TenhouCLient] = [] #List of all wgThreads
    wgClient = []

    def HasHashTag(self,group_id,hashTag)->bool: #hashTag: xxxx
        if hashTag not in self.AllHashTags():
            return False
        else:
            return self.wgClient[self.AllHashTags().index(hashTag)].hasGroup(group_id)

    def ClientIndex(self,WG:str) -> int:
        for i in range(len(self.wgClient)):
            if self.wgClient[i].WG == WG:
                return i
        return -1

    def AllWgGames(self) -> list:
        res = []
        for i in self.wgClient:
            res.append(str(i.WG))
        return res

    def AllHashTags(self) -> list:
        res = []
        for i in self.wgClient:
            res.append(str(i.hashTag))
        return res
    
    def ClearEndedClient(self):
        i = 0
        while i < len(self.wgClient):
            print("Checking end flag "+str(i))
            if (self.wgClient[i].clientEnds == True):
                print("Poping "+str(i))
                self.wgClient.pop(i)
            else:
                print("Not clearing "+str(i))
                i+=1
    
    def ForceCloseAllClient(self):
        i = 0
        while i < len(self.wgClient):
            self.wgClient[i].end_game()

    def StartWG(self,WG,startTime,gameType):
        self.wgClient.append(wglive.TenhouCLient(WG,getTag(),startTime,gameType))

    def wgSche2(self):
        print("Checking for new wg...")
        # Clear up
        self.ClearEndedClient()
        # Add new WG
        with open("/root/QQ/QQ-Group-Repeater/wglist.json",'r',encoding='utf-8') as load_f:
            load_dict = json.load(load_f)
        session = HTMLSession()
        r = session.get(url)
        res = (r.text)[6:-5].split(",\r\n")

        checkedname = []
        for game in res:
            game = game[1:-1].split(",")
            #generate gametime
            t = (game[2]).split(":")
            t_h = int(t[0])-1
            if t_h < 0:
                t_h = 23
            t_m = int(t[1])
            now = datetime.datetime.now()
            gtime = 0
            if(now.hour==23 and t_h==0):
                nday = now+datetime.timedelta(days=1)
                gtime = int(time.mktime(datetime.datetime(nday.year,nday.month,nday.day,t_h,t_m,0).timetuple()))
            gtime = int(time.mktime(datetime.datetime(now.year,now.month,now.day,t_h,t_m,0).timetuple()))

            i = 4
            count = -1
            while i < len(game):
                count += 1
                #game WGtag
                WGtag = str(game[0])
                #generate pname
                name = base64.b64decode(game[i]).decode()
                for k in load_dict:
                    if((k['id'] not in checkedname) and (k['id'] == name) and gtime > k['currgame']):
                        print("Handling player "+k['id']) 
                        k['currgame'] = gtime
                        #IF GAME not in WG: Add this game first
                        if WGtag not in self.AllWgGames():
                            if t_m < 10:
                                stime = str(t_h)+":0"+str(t_m)
                            else:
                                stime = str(t_h)+":"+str(t_m)
                            self.StartWG(WGtag,stime,game[3])
                        #Add this group and player
                        ind = self.ClientIndex(WGtag)
                        print("INDEX: "+str(ind))
                        while ((not self.wgClient[ind].is_wg) and (self.wgClient[ind].game_is_continue)):
                            for gid in k['groupid']:
                                self.wgClient[self.ClientIndex(WGtag)].addQQ(gid,k['id'])
                i += 3
        # EndCheck
        print("Writing Back... to wglist.json")
        with open("/root/QQ/QQ-Group-Repeater/wglist.json",'w',encoding='utf-8') as f:
            f.write(json.dumps(load_dict,ensure_ascii=False))
    
    
