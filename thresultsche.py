import coolq
import asyncio

import json
from Repeater import aioGet
from Bot import Bot
import wg
import time
import requests
import urllib.parse
import random
import tenhou2

url = "https://nodocchi.moe/api/listuser.php?name="
msgRank =( 
        [[["轻松拿下一位, 真的太强了","轻松拿下一位, 全程乱杀"],
        ["精通避三, 避免了重大损失","获得一个二位, 深藏功与名"],
        ["被安排了一个三位, 一定是角田的阴谋","被安排了一个三位, 实在是太苦了"]],
        [["轻松拿下一位, 真的太强了","轻松拿下一位, 全程乱杀"],
        ["获得一个二位, 深藏功与名"],
        ["精通避四, 避免了重大损失","精通避四, 不掉分就是胜利"],
        ["被安排了一个四位, 一定是角田的阴谋","被安排了一个四位, 实在是太苦了"]]])

async def thResSche():
    print("In TH res fetching")

    with open("/root/QQ/QQ-Group-Repeater/wglist.json",'r',encoding='utf-8') as load_f:
        load_dict = json.load(load_f)


    for i in load_dict:
        name = i["id"]
        if(i["recentgame"] != []):
            r = requests.get(url+urllib.parse.quote(str(name)))
            res = json.loads(r.text)
            index = -1
            lastmatch = 0
            while True:
                lastmatch = res["list"][index]
                if (lastmatch["sctype"] == "a") or(lastmatch["playerlevel"] == "0")or(lastmatch["playerlevel"] == "1"):
                    index = index - 1
                else:
                    break
            if((int(lastmatch["starttime"])+300) in i["recentgame"]):
                i["recentgame"].remove(int(lastmatch["starttime"])+300)
                with open("/root/QQ/QQ-Group-Repeater/wglist.json",'w',encoding='utf-8') as f:
                    json.dump(load_dict, f,ensure_ascii=False)
                msg = ""
                gamemode = int(lastmatch["playernum"])
                rank = 0
                for j in range(1,gamemode+1):
                    if(lastmatch["player"+str(j)] == name):
                        rank = j
                msglist = msgRank[gamemode-3][rank-1]
                msg = msg+name+" "+msglist[random.randint(0,len(msglist)-1)]+"\n"

                if (lastmatch["playernum"] == "3"):
                    msg = msg + "三"
                else:
                    msg = msg + "四"
                
                if (lastmatch["playerlevel"] == "0"):
                    msg = msg + "般"
                elif (lastmatch["playerlevel"] == "1"):
                    msg = msg + "上"
                elif (lastmatch["playerlevel"] == "2"):
                    msg = msg + "特"
                elif (lastmatch["playerlevel"] == "3"):
                    msg = msg + "鳳"

                if (lastmatch["playlength"] == "1"):
                    msg = msg + "东"
                elif (lastmatch["playlength"] == "2"):
                    msg = msg + "南"
                
                if (lastmatch["kuitanari"] == "1"):
                    msg = msg + "喰"
                
                if (lastmatch["akaari"] == "1"):
                    msg = msg + "赤"
                
                msg = msg + " "
                timeT = int(lastmatch["starttime"])+int(lastmatch["during"])*60
                timeT = time.localtime(timeT)
                th = timeT.tm_hour
                tm = timeT.tm_min
                if th < 10:
                    th = "0" + str(th)
                else:
                    th = str(th)
                if tm < 10:
                    tm = "0" + str(tm)
                else:
                    tm = str(tm)
                msg = msg + " " + str(th)+":" + str(tm)+"\n"

                if "url" in lastmatch:
                    msg = msg + lastmatch["url"]+"\n"
                
                if(lastmatch["playernum"] == "4"):
                    ptadd = [35,5,-15,-25]
                    for j in range (1,5):
                        msg = msg + lastmatch["player"+str(j)]+ "\t"
                        pt = lastmatch["player"+str(j)+"ptr"]
                        msg = msg + str(int(round((float(pt)-ptadd[j-1]),1)*1000)+25000) + "("+str(pt)+")\n"
                else:
                    ptadd = [30,-5,-25]
                    for j in range (1,4):
                        msg = msg + lastmatch["player"+str(j)]+ "\t"
                        pt = lastmatch["player"+str(j)+"ptr"]
                        msg = msg + str(int(round((float(pt)-ptadd[j-1]),1)*1000)+35000) + "("+str(pt)+")\n"
                
                if(lastmatch["playernum"] == "4"):
                    (lastrank,lastpt) = tenhou2.getRank(res["list"][0:-1],name)
                    msg = msg + tenhou2.levelmap[lastrank]['name']+ " " + str(lastpt) + "pt --> "
                    ptDelta = 0
                    length = int(res["list"][-1]["playlength"])
                    lv = res["list"][-1]["playerlevel"]
                    if rank == 4:
                        ptDelta = 0 - tenhou2.levelmap[lastrank]['losescore'][length-1]
                    else:
                        ptDelta = tenhou2.ptchange['4'][length-1][lv][rank-1]
                    currpt = lastpt
                    currank = lastrank
                    currpt = currpt + ptDelta
                    if(currpt >= tenhou2.levelmap[currank]['maxscore']):
                        currank = currank + 1
                        currpt = tenhou2.levelmap[currank]['initscore']
                    #print("\t升段至 "+levelmap[currank]['name'])
                    elif(currpt < 0 ):
                        if(tenhou2.levelmap[currank]['haslower'] == True):
                            currank = currank - 1
                            currpt = tenhou2.levelmap[currank]['initscore']
                        #print("\t降段至 "+levelmap[currank]['name'])
                        else:
                            currpt = 0
                    msg = msg + tenhou2.levelmap[currank]['name']+ " " + str(currpt)+"pt"
                
                for group_id in i["groupid"]:
                        print("before" + str(group_id))
                        await coolq.bot.send({'group_id': group_id}, message=msg)
                        print("after" +str(group_id))
                        #time.sleep(1)

loop = asyncio.get_event_loop()
result = loop.run_until_complete(thResSche())
loop.close()
