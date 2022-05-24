from itertools import count
import coolq
import asyncio

import json
from Repeater import aioGet
from Bot import Bot
import wg
import time
import requests

url = "https://nodocchi.moe/s/wg.js"
wgurl = "http://tenhou.net/0/?wg="

async def wgSche():
    print("In wg checking")

    with open("/root/QQ/QQ-Group-Repeater/wglist.json",'r',encoding='utf-8') as load_f:
        load_dict = json.load(load_f)

    r = requests.get(url)
    res = json.loads(r.text)

    checkedname = []
    for i in res:
        count = -1
        for j in i["players"]:
            count = count+1
            for k in load_dict:
                if (k['id'] not in checkedname) and (k['id'] == j['name']) and (i["info"]["id"] != k["currgame"]):
                    checkedname.append(k['id'])
                    k["currgame"] = i["info"]["id"]
                    with open("/root/QQ/QQ-Group-Repeater/wglist.json",'w',encoding='utf-8') as f:
                        json.dump(load_dict, f,ensure_ascii=False)
                    msg = k['id']+" 正在乱杀, 快来围观:\n"
                    if (i["info"]["playernum"] == 4):
                        msg = msg + "四"
                    elif (i["info"]["playernum"] == 3):
                        msg = msg + "三"

                    if (i["info"]["playerlevel"] == 2):
                        msg = msg + "特"
                    elif (i["info"]["playerlevel"] == 3):
                        msg = msg + "鳳"
                    
                    if (i["info"]["playlength"] == 1):
                        msg = msg + "东"
                    elif (i["info"]["playlength"] == 2):
                        msg = msg + "南"

                    if (i["info"]["kuitanari"] == 1):
                        msg = msg + "喰"
                    
                    if (i["info"]["akaari"] == 1):
                        msg = msg + "赤"

                    if (i["info"]["rapid"] == 1):
                        msg = msg + "速"

                    t = time.localtime(i["info"]["starttime"])
                    msg = msg + " " + str(t.tm_hour)+":" + str(t.tm_min)+"\n"

                    msg = msg + wgurl + i["info"]["id"]+"&tw="+str(count)+"\n"
                    msg = msg + (i["players"][0]["name"]+ " " + i["players"][1]["name"]+" " 
                              + i["players"][2]["name"])
                    if (i["info"]["playernum"] == 4):
                        msg = msg + " " + i["players"][3]["name"]

                    for group_id in k["groupid"]:
                        print(group_id)
                        await coolq.bot.send({'group_id': group_id}, message=msg)
                        time.sleep(1)

loop = asyncio.get_event_loop()
result = loop.run_until_complete(wgSche())
loop.close()
