import json
import urllib.parse
import requests


url = "https://nodocchi.moe/api/listuser.php?name="
wgurl = "https://nodocchi.moe/s/wg.js"
def wgadd(id,group):
    id = str(id)
    tar = url+urllib.parse.quote(id)
    r = requests.get(tar)
    res = json.loads(r.text)
    if(res == False):
        return "没有找到该玩家!"
    with open("wglist.json",'r',encoding='utf-8') as load_f:
        load_dict = json.load(load_f)
    for i in load_dict:
        if(i['id'] == id ):
            if (group in i['groupid']):
                return "已经关注过["+id+"]啦"
            else:
                i['groupid'].append(group)
                with open("wglist.json",'w',encoding='utf-8') as f:
                    json.dump(load_dict, f,ensure_ascii=False)
                return "新增关注["+id+"]"
    with open("wglist.json",'w',encoding='utf-8') as f:
        newadd = {'id': id,'groupid':[group], 'currgame':'', "recentgame": []}
        load_dict.append(newadd)
        json.dump(load_dict, f,ensure_ascii=False)
        return "新增关注["+id+"]"

def wgdel(id,group):
    id = str(id)
    tar = url+urllib.parse.quote(id)
    r = requests.get(tar)
    res = json.loads(r.text)
    if(res == False):
        return "没有找到该玩家!"
    with open("wglist.json",'r',encoding='utf-8') as load_f:
        load_dict = json.load(load_f)
    for i in load_dict:
        if(i['id'] == id ):
            if (group in i['groupid']):
                i['groupid'].remove(group)
                if(i['groupid'] == []):
                    load_dict.remove(i)
                with open("wglist.json",'w',encoding='utf-8') as f:
                    json.dump(load_dict, f,ensure_ascii=False)
                return("不再关注["+id+"]了")
            else:
                return("啊这,好像还没有关注["+id+"]呢")
    return("啊这,好像还没有关注["+id+"]呢")

def wglist(group):
    with open("wglist.json",'r',encoding='utf-8') as load_f:
        load_dict = json.load(load_f)
    ans = "本群关注:"
    for i in load_dict:
        if (group in i['groupid']):
            ans = ans+"\n"+i['id']
    if ans == "本群关注:":
        return "本群暂无观战玩家~"
    else:
        return ans

def wgsync():
    print("On syncing TH score...")
    with open("wglist.json",'r',encoding='utf-8') as load_f:
        load_dict = json.load(load_f)
    
    rwg = requests.get(wgurl)
    reswg = json.loads(rwg.text)
    for i in reswg:
        for j in i["players"]:
            for k in load_dict:
                if (k['id'] == j['name']):
                    if(i["info"]["starttime"] not in k["recentgame"]):
                        k["recentgame"].append(i["info"]["starttime"])

    with open("/root/QQ/QQ-Group-Repeater/wglist.json",'w',encoding='utf-8') as f:
                json.dump(load_dict, f,ensure_ascii=False)
    print("Sync TH score complete.")
    