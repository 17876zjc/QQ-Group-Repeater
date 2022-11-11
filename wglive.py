import socket
from threading import Thread
from urllib.parse import quote
from time import sleep
import random
import re

import urllib.parse
import coolq
import asyncio

from bot_p import bot

msgRank =( 
        [[["轻松拿下一位, 真的太强了","轻松拿下一位, 全程乱杀","太强了轻松获得了一位"],
        ["精通避三, 避免了重大损失","获得一个二位, 深藏功与名"],
        ["被安排了一个三位, 一定是角田的阴谋","被安排了一个三位, 实在是太苦了","打的根本不差,显然是波","被安排了一个三位,实在是时运不济"]],
        [["轻松拿下一位, 真的太强了","轻松拿下一位, 全程乱杀","太强了轻松获得了一位"],
        ["获得一个二位, 深藏功与名"],
        ["精通避四, 避免了重大损失","精通避四, 不掉分就是胜利"],
        ["被安排了一个四位, 一定是角田的阴谋","被安排了一个四位, 实在是太苦了","打的根本不差,显然是波","被安排了一个四位,实在是时运不济"]]])
wgurl = "http://tenhou.net/0/?wg="
KyokuName = {0:"东一局",1:"东二局",2:"东三局",3:"东四局",
             4:"南一局",5:"南二局",6:"南三局",7:"南四局",
             8:"西一局",9:"西二局",10:"西三局",11:"西四局"}
YakuName = {0: "自摸",
            1: "立直",
            2: "一发",
            3: "抢杠",
            4: "岭上开花",
            5: "海底捞月",
            6: "河底捞鱼",
            7: "平和",
            8: "断幺九",
            9: "一杯口",
            10: "自风东",
            11: "自风南",
            12: "自风西",
            13: "自风北",
            14: "场风东",
            15: "场风南",
            16: "场风西",
            17: "场风北",
            18: "役牌白",
            19: "役牌发",
            20: "役牌中",
            21: "两立直",
            22: "七对子",
            23: "混全带幺九",
            24: "一气通贯",
            25: "三色同顺",
            26: "三色同刻",
            27: "三杠子",
            28: "对对和",
            29: "三暗刻",
            30: "小三元",
            31: "混老头",
            32: "两杯口",
            33: "纯全带幺九",
            34: "混一色",
            35: "清一色",

            36: "人和",
            37: "天和",
            38: "地和",
            39: "大三元",
            40: "四暗刻",
            41: "四暗刻单骑",
            42: "字一色",
            43: "绿一色",
            44: "清老头",
            45: "九莲宝灯",
            46: "纯正九莲宝灯",
            47: "国士无双",
            48: "国士无双十三面",
            49: "大四喜",
            50: "小四喜",
            51: "四杠子",

            52: "宝牌",
            53: "里宝牌",
            54: "赤宝牌"}

TENHOU_HOST = "133.242.10.78"
TENHOU_PORT = 10080
USER_ID = "NoName"


class TenhouCLient:
    WG = ""
    hashTag = ""
    indetail = False
    #Client Data
    socket = None
    game_is_continue = True
    keep_alive_thread = None
    wg_thread = None
    is_wg = False
    clientEnds = False
    #Player Data
    pname = ["","","",""]
    prank = [0,0,0,0]
    pR = [0,0,0,0]
    #Game Data
    startTime = "00:00"
    gametype = ""
    kyoku = -1
    honba = -1
    ten = [0,0,0,0]
    #QQ Data
    qq = [] #{'group':1234,'player':[0,1],'isdetail':False,'hasreported':False}

    def getGameType(self) -> str:
        res = ""
        i = bin(int(self.gametype))[2:]
        i = '0'*(8-len(i))+i
        if i[3] == '1':
            res += "三"
        else:
            res += "四"

        if i[0] == '1' and i[2] == '1':
            res += "鳳"
        elif i[2] == '1':
            res += "特"
        
        if i[4] == '1':
            res += "南"
        else: 
            res += "東"
        
        if i[5] == '0':
            res += "喰"
        
        if i[6] == '0':
            res += "赤"

        if i[1] == '1':
            res += "速"
        

    def addQQ(self,group:int,pname:str):
        hasQQ = False
        while(self.pname == ["","","",""] and not self.clientEnds):
            continue
        #Find player id
        pid = self.pname.index(pname)
        for i in self.qq:
            if i['group'] == group:
                hasQQ = True
                if pid not in i['player']:
                    i['player'].append(pid)
                break
        if not hasQQ:
            self.qq.append({'group':group,'player':[pid],'isdetail':False,'hasreported':False})
    
    def rmQQ(self,group:int):
        for i in self.qq:
            if (i['group'] == group):
                self.qq.remove(i)
                if self.qq == []:
                    self.end_game()
                break
    def addDetail(self,group:int):
        for i in self.qq:
            if i['group'] == group:
                i['isdetail'] = True
                self.indetail = True
                break
    def rmDetail(self,group:int):
        for i in self.qq:
            if i['group'] == group:
                i['isdetail'] = False
                break
        needDetail = False
        for i in self.qq:
            if i['isdetail'] == True:
                needDetail = True
                break
        self.indetail = needDetail

    def hasGroup(self,group_id) ->bool:
        for i in self.qq:
            if i['group'] == group_id:
                return True
        return False

    def qqSendMsg(self,group_id,msg):

        async def sendMsg(group_id,msg):
            await bot.send({'group_id': group_id}, message=msg)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(sendMsg(group_id,msg))
        loop.close()

    def sendGameStartMsg(self):
        res = "正在乱杀, 快来围观:\n#"+self.hashTag+" 【对局开始】 "+self.getGameType()+" "+self.startTime+"\n"
        res = res + wgurl + self.WG+"\n"
        for i in self.pname:
            res = res + i + " "
        for i in self.qq:
            if (i['hasreported'] == False):
                i['hasreported'] = True
                temp = ""
                for j in range(len(i['player'])):
                    temp += self.pname[i['player'][j]]
                    if j != len(i['player'])-1:
                        temp+=","
                res = temp+" "+res
                self.qqSendMsg(i['group'],res)

    def reportGameDetail(self,group_id):
        res = ""
        res = res +"#"+self.hashTag+" "+self.getGameType+" "
        if (self.ten == [0,0,0,0]):
            res += "【等待中】\n"
            for i in self.pname:
                res = res + i +" "
        else:
            res += "【对局中】\n"
            res += KyokuName[self.kyoku]
            res += " "
            res += self.honba
            res += "本场\n"
            for i in range(4):
                res += self.pname[i]
                res += " "
                res += self.ten[i]
                res += "\n"
        self.qqSendMsg(group_id,res)

    def _random_sleep(self, min_sleep, max_sleep):
        sleep(random.uniform(min_sleep, max_sleep))

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(1)
        self.socket.connect((TENHOU_HOST, TENHOU_PORT))

    def _send_message(self, message):
        # tenhou requires an empty byte in the end of each sending message
        message += "\0"
        self.socket.sendall(message.encode())

    def _read_message(self):
        try:
            message = self.socket.recv(4096)
            return message.decode("utf-8")
        except Exception:
            return ""

    def _get_multiple_messages(self):
        # tenhou can send multiple messages in one request
        messages = self._read_message()
        #print("Receive message: " + messages)
        if not messages:
            return []
        messages = messages.split("\x00")
        # last message always is empty after split, so let's exclude it
        messages = messages[0:-1]
        for message in messages:
            print("Received : " + message)
        return messages
    
    def _send_keep_alive_ping(self):
        def send_request():
            while self.game_is_continue:
                #print("Sending Awake")
                self._send_message("<Z />")
                #if self.is_wg == False:
                    #self._send_message('<PXR V="1" />')

                # we can't use sleep(15), because we want to be able
                # end thread in the middle of running
                seconds_to_sleep = 15
                for _ in range(0, seconds_to_sleep * 2):
                    if self.game_is_continue:
                        sleep(0.5)

        self.keep_alive_thread = Thread(target=send_request)
        self.keep_alive_thread.start()

    def authenticate(self):
        self._send_message('<HELO name="{}" tid="f0" sx="F" />'.format(quote(USER_ID)))
        messages = self._get_multiple_messages()
        auth_message = messages[0]

        if not auth_message:
            print("Auth message wasn't received")
            return False
        # sometimes tenhou send an empty tag after authentication (in tournament mode)
        # and bot thinks that he was not auth
        # to prevent it lets wait a little bit
        # and lets read a group of tags
        continue_reading = True
        counter = 0
        authenticated = False
        while continue_reading:
            messages = self._get_multiple_messages()
            for message in messages:
                if "<LN" in message:
                    authenticated = True
                    continue_reading = False

            counter += 1
            # to avoid infinity loop
            if counter > 10:
                continue_reading = False

        if authenticated:
            self._send_keep_alive_ping()
            print("Successfully authenticated")
            return True
        else:
            print("Failed to authenticate")
            return False

    def end_game(self, success=True):
        self.game_is_continue = False
        if self.socket:
            self._send_message("<BYE />")
        if self.keep_alive_thread:
            self.keep_alive_thread.join()
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
            self.socket.close()
        except OSError:
            pass
        self.clientEnds = True
    
    def InitplayerData(self,message):
        #InitName
        self.pname[0] = str(urllib.parse.unquote(re.findall(r'n0=".*?"',message)[0][4:-1]))
        self.pname[1] = str(urllib.parse.unquote(re.findall(r'n1=".*?"',message)[0][4:-1]))
        self.pname[2] = str(urllib.parse.unquote(re.findall(r'n2=".*?"',message)[0][4:-1]))
        self.pname[3] = str(urllib.parse.unquote(re.findall(r'n3=".*?"',message)[0][4:-1]))
        #InitRank
        t = re.findall(r'dan=".*?"',message)[0][5:-1].split(",")
        self.prank[0] = int(t[0])
        self.prank[1] = int(t[1])
        self.prank[2] = int(t[2])
        self.prank[3] = int(t[3])
        #InitR
        t = re.findall(r'rate=".*?"',message)[0][6:-1].split(",")
        self.pR[0] = float(t[0])
        self.pR[0] = float(t[1])
        self.pR[0] = float(t[2])
        self.pR[0] = float(t[3])

    def UploadGameProcess(self,message): # an <INIT ... >
        # Kyoku and Honba
        t = re.findall(r'seed=".*?"',message)[0][6:-1].split(",")
        self.kyoku = int(t[0])
        self.honba = int(t[1])
        # Point
        t = re.findall(r'ten=".*?"',message)[0][5:-1].split(",")
        self.ten[0] = int(t[0])
        self.ten[1] = int(t[1])
        self.ten[2] = int(t[2])
        self.ten[3] = int(t[3])
        pass

    def analyOneTile(self,tile:int):
        number = 0
        color = ""
        if (int(tile / 36) == 0):
            color = "m"
        elif (int(tile / 36) == 1):
            color = "p"
        elif (int(tile / 36) == 2):
            color = "s"
        else:
            color = "z"

        t = tile%36
        if (int(tile/36) < 3 and int(t/4) == 4 and t%4 == 0):
            number = 0
        else:
            number = int(t/4)+1

        return [number,color]

    def analyOneMelt(self,message:int):
        res = ""
        code = bin(message)[2:]
        if(code[-3] == '1'): #Chi
            Base = int (int(code[:-10],2) / 3)
            for i in range(3):
                if(Base%7 + i == 4 and int(code[int(-5-2*i):int(-3-2*i)],2) == 0): #Is an aka 5
                    res += '0'
                else:
                    res += str(Base%7+i+1)
            if (int(Base/7) == 0):
                res += 'm'
            elif (int(Base/7) == 1):
                res += 'p'
            else:
                res += 's'
            return res
        elif (code [-4] == '1'): #Pon
            Base = int (int(code[:-9],2) / 3)
            [number,color] = self.analyOneTile(Base*4)
            if (color != "z" and number == 5 and int(code[9:11],2) != 0): #An aka poned
                res += ('055'+color)
            else:
                res += (str(number)*3+color)
            return res
        elif (code [-5] == '1'): #Kakan
            Base = int (int(code[:-9],2) / 3)
            [number,color] = self.analyOneTile(Base*4)
            if (color != "z" and number == 5):
                res += ('0555'+color)
            else:
                res += (str(number)*4+color)
            return res
        else: #Ankang
            Base = int(code[:-10],2)
            [number,color] = self.analyOneTile(Base)
            if(color != "z" and number == 5):
                res += ('口05口'+color)
            else:
                res += ('口'+str(number)*2+'口'+color)
            return res

    def getPlayerRank(self,pindex):
        res = 1
        pten = self.ten[pindex]
        for i in range(4):
            if self.ten[i] > pten:
                res += 1
            elif self.ten[i] == pten and i > pindex:
                res += 1
        return res
                

    def ReportEndGame(self,message:list):
        self.game_is_continue = False
        res = "【对局结束】 #"+self.hashTag+"\n"
        for i in range(4):
            res += (self.pname[i] + " "+message[i*2]+"00 ("+message[i*2+1]+")\n")

        temp = ""
        for i in self.qq:
            for j in i['player']:
                temp += self.pname[j]
                msglist = msgRank[1][self.getPlayerRank(j)-1]
                temp += " "
                temp += msglist[random.randint(0,len(msglist)-1)]
                temp += "\n" 
            res = temp + res
            self.qqSendMsg(i['group'],res)
        

    def ReportAgari(self,message): # <AGARI ... >
        res = ""
        # Kyoku, Honba
        res += (KyokuName[self.kyoku] + " " + str(self.honba) + "本场 ")
        # Players
        p1 = int(re.findall(r'who=".*?"',message)[0][5:-1])
        p2 = int(re.findall(r'fromWho=".*?"',message)[0][9:-1])
        res += (self.pname[p1] + " ")
        if (p1 == p2):
            res += "自摸"
        else:
            res += ("荣 " + self.pname[p2])
        point = (re.findall(r'ten=".*?"',message)[0][5:-1]).split(",")[1]
        res += (" "+point)
        if "owari" in message:
            res += " 【终局】\n"
        else:
            res +="\n"
        # Read Hand:
        machi = re.findall(r'machi=".*?"',message)[0][7:-1]
        
        hand = ""
        hai = re.findall(r'hai=".*?"',message)[0][5:-1].split(",")
        hai.remove(machi)

        for i in range(len(hai)):
            tile = int(hai[i])
            [number,color] = self.analyOneTile(tile)
            hand = hand + str(number)
            if((i == len(hai)-1) or (self.analyOneTile(int(hai[i+1]))[1] != color)):
                hand  = hand + str(color)
        res += hand
        # Read Melt
        if (re.findall(r'm=".*?"',message)!= []):
            melt = ""
            m = re.findall(r'm=".*?"',message)[0][3:-1].split(",")
            for i in m:
                melt += " "
                melt += self.analyOneMelt(int(i))
            res += melt
        
        [number,color] = self.analyOneTile(int(machi))
        res += (" "+str(number) + color + "\n")

        # Read Yaku
        if (re.findall(r'yaku=".*?"',message)!=[]):
            y = re.findall(r'yaku=".*?"',message)[0][6:-1].split(",")
            i = 0
            while (i < len(y)):
                res += (y[i+1] + " ")
                res += (YakuName[int(y[i])] + "\n")
                i += 2 
        else:
            y = re.findall(r'yakuman=".*?"',message)[0][9:-1].split(",")
            for i in y:
                res += ("1 "+ YakuName[(int(y[i]))] + "\n")
        
        # Read Point Change
        s = re.findall(r'sc=".*?"',message)[0][4:-1].split(",")
        i = 0
        while (2 * i < len(s)):
            res += (self.pname[i] + " ")
            oldscore = int(s[i*2])*100
            dscore = int(s[i*2+1])*100
            res += (str(oldscore)+" -> "+str(oldscore+dscore)+"\n")
            self.ten[i] = oldscore+dscore
            i+=1
        
        for i in self.qq:
            if i['isdetail'] == True:
                self.qqSendMsg(i['group'],res)
        #print(res)
        if(re.findall(r'owari=".*?"',message)!=[]):
            self.ReportEndGame(re.findall(r'owari=".*?"',message)[0][7:-1].split(","))

    def ReportRyuukyoku(self,message): #<RYUUKYOKU ...>
        res = ""
        # Kyoku, Honba
        res += (KyokuName[self.kyoku] + " " + str(self.honba) + "本场 ")
        # Ryuukyuku type
        if (re.findall(r'type=".*?"',message) ==[]):
            res +="流局"
        else:
            type = re.findall(r'type=".*?"',message)[0][6:-1]
            if type == "yao9":
                res += "九种九牌"
            elif type == "reach4":
                res += "四家立直"
            elif type == "ron3":
                res += "三家和了"
            elif type == "kan4":
                res += "四杠散了"
            elif type == "kaze4":
                res += "四风连打"
            elif type == "nm":
                res += "流局满贯"

        if "owari" in message:
            res += " 【终局】\n"
        else:
            res +="\n"
        # Read Point Change
        s = re.findall(r'sc=".*?"',message)[0][4:-1].split(",")
        i = 0
        while (2 * i < len(s)):
            res += (self.pname[i] + " ")
            oldscore = int(s[i*2])*100
            dscore = int(s[i*2+1])*100
            self.ten[i] = oldscore+dscore
            res += (str(oldscore)+" -> "+str(oldscore+dscore)+"\n")
            i+=1
        
        for i in self.qq:
            if i['isdetail'] == True:
                self.qqSendMsg(i['group'],res)
        #print(res)
        if(re.findall(r'owari=".*?"',message)!=[]):
            self.ReportEndGame(re.findall(r'owari=".*?"',message)[0][7:-1].split(","))

    def wg(self):
        print("Start to wg: "+ str(self.WG))
        self._send_message('<CHAT text="%2Fwg%20{}" />'.format(quote(self.WG)))
        self._random_sleep(1, 2)

        while self.game_is_continue and not self.clientEnds:
            self._random_sleep(1, 2)
            messages = self._get_multiple_messages()


            for message in messages:
                if(self.is_wg == False): #When waiting for wg start
                    if "<ERR" in message: #围观错误
                        print("WG Error, quiting...")
                        self.game_is_continue = False
                        break
                    if "<GO" in message:
                        self.is_wg = True
                        self._random_sleep(1, 2)
                        self._send_message("<GOK />")
                else: #Already in wg
                    self.sendGameStartMsg()
                    if "<UN" in message: #Init player data
                        self.InitplayerData(re.findall(r'<UN .*?>',message)[0])
                    if "<AGARI" in message: #Agari
                        self.ReportAgari(re.findall(r'<AGARI .*?>',message)[0])
                    if "<RYUUKYOKU" in message: #Ryuukyoku
                        self.ReportRyuukyoku(re.findall(r'<RYUUKYOKU .*?>',message)[0])
                    if "<INIT" in message: #Update GameProcess
                        self.UploadGameProcess(re.findall(r'<INIT .*?>',message)[0])

        self.end_game()

    def __init__(self,WG,hashTag,startTime,gametype) -> None:
        self.WG = WG
        self.hashTag = hashTag
        self.startTime = startTime
        self.gametype = gametype
        self.connect()
        auth = self.authenticate()
        if auth:
            try:
                self.wg_thread = Thread(target=self.wg)
                self.wg_thread.start()
            except Exception as e:
                print("Exception occured")
                self.end_game()
        else:
            self.clientEnds = True
            print("Auth false")
            self.end_game()

    def __del__(self):
        if self.wg_thread:
            self.wg_thread.join()

#if __name__ == "__main__":
    #client = TenhouCLient('B49639AB','')
    #client.connect()
    #auth = client.authenticate()
    #try:
    #    if auth:
    #        client.wg()
    #except KeyboardInterrupt:
    #    print("Exiting...")
    #    client.end_game()
    #except Exception as e:
    #    print("Error: "+str(e))
    #    print("Exiting...")
    #    client.end_game()
