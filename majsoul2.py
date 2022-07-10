import requests
import json
import time

tablech = ["王座","王座东","玉","玉东","金","金东"]
table4 = ["16","15","12","11","9","8"]
table3 = ["26","25","24","23","22","21"]

ranktable = {
    "10301" : "雀杰一",
    "10302" : "雀杰二",
    "10303" : "雀杰三",
    "10401" : "雀豪一",
    "10402" : "雀豪二",
    "10403" : "雀豪三",
    "10501" : "雀圣一",
    "10502" : "雀圣二",
    "10503" : "雀圣三",
    "10701" : "魂天Lv1",
    "10702" : "魂天Lv2",
    "10703" : "魂天Lv3",
    "10704" : "魂天Lv4",
    "10705" : "魂天Lv5",
    "10706" : "魂天Lv6",
    "10707" : "魂天Lv7",
    "10708" : "魂天Lv8",
    "10709" : "魂天Lv9",
    "10710" : "魂天Lv10",
    "10711" : "魂天Lv11",
    "10712" : "魂天Lv12",
    "10713" : "魂天Lv13",
    "10714" : "魂天Lv14",
    "10715" : "魂天Lv15",
    "10716" : "魂天Lv16",
    "10717" : "魂天Lv17",
    "10718" : "魂天Lv18",
    "10719" : "魂天Lv19",
    "10720" : "魂天Lv20"
}

rankptMax = {
    "10301" : "1600",
    "10302" : "2000",
    "10303" : "2400",
    "10401" : "2800",
    "10402" : "3200",
    "10403" : "3600",
    "10501" : "4000",
    "10502" : "6000",
    "10503" : "9000",
    "10701" : "20.0",
    "10702" : "20.0",
    "10703" : "20.0",
    "10704" : "20.0",
    "10705" : "20.0",
    "10706" : "20.0",
    "10707" : "20.0",
    "10708" : "20.0",
    "10709" : "20.0",
    "10710" : "20.0",
    "10711" : "20.0",
    "10712" : "20.0",
    "10713" : "20.0",
    "10714" : "20.0",
    "10715" : "20.0",
    "10716" : "20.0",
    "10717" : "20.0",
    "10718" : "20.0",
    "10719" : "20.0",
    "10720" : "20.0",
    }

urlquery = "https://ak-data-1.sapk.ch/api/v2/pl4/search_player/name?limit=20"
url4_1 = "https://ak-data-1.sapk.ch/api/v2/pl4/player_stats/ID/1262304000000/TIME9999?mode=16.12.9.15.11.8&tag=459520"
url4_2 = "https://ak-data-6.pikapika.me/api/v2/pl4/player_extended_stats/ID/1262304000000/TIME9999?mode=16.12.9.15.11.8&tag=460396"

url3_1 = "https://ak-data-6.pikapika.me/api/v2/pl3/player_stats/ID/1262304000000/TIME9999?mode=26.25.24.23.22.21&tag=460401"
url3_2 = "https://ak-data-6.pikapika.me/api/v2/pl3/player_extended_stats/ID/1262304000000/TIME9999?mode=26.25.24.23.22.21&tag=460401"

def getid(name,mode = 4):
    tar = urlquery.replace("name", name)
    if (mode == 3):
        tar = tar.replace("pl4","pl3")
    r = requests.get(tar)
    res = json.loads(r.text)

    if len(res) == 0:
        return ["",None]
    # 可能会有多个结果，这里就当只有一个了
    return [res[0]['nickname'],res[0]['id']]

def getmodes(id,mode = 4):
    if(mode == 3):
        tar = url3_1.replace("ID",str(id))
    else:
        tar = url4_1.replace("ID",str(id))
    tar = tar.replace("TIME",str(int(time.time())))
    r = requests.get(tar)
    res = json.loads(r.text)
    return res["played_modes"]


def searchQueHun2(name,mode = 4):
    table = []
    if(name.find(" ")>=0):
        listname = list(name)
        listname.reverse()
        reversename = ''.join(listname)
        index = len(name) - reversename.find(" ")
        test = name[index:]
        name = name[:(index-1)]
        while(1):
            if(test.find("+") >= 0):
                tt = test[:test.find("+")]
                test = test[test.find("+")+1:]
                if(tt in tablech):
                    table.append(tt)
                else:
                    return ("输入的场次 "+tt+" 找不到呢~")
            else:
                if(test in tablech):
                    table.append(test)
                    break
                else:
                    return ("输入的场次 "+test+" 找不到呢~")
    
    [name,id] = getid(name,mode)
    if(id == None):
        return "没有查到呢~"

    modes = getmodes(id)
    for i in table:
        if int(table4[tablech.index(i)]) not in modes:
            error = "没有找到在"
            if(mode == 4):
                error += "<四麻>"
            else:
                error += "<三麻>"
            error += ("["+i+"]的对战!\n试一试对这位玩家搜索")
            for k in modes:
                    if mode == 4:
                        error += (" [" + tablech[table4.index(k)] + "]")
                    else:
                        error += (" [" + tablech[table3.index(k)] + "]")
            return error

    if mode == 3:
        modethis = "26.25.24.23.22.21"
    else:
        modethis = "16.12.9.15.11.8"

    res = name + "\n查询范围:"
    if (table  == []):
        res += " 全部对局\n\n"
    else:
        modethis = ""
        for i in table:
            res +=(" ["+i+"]")
            if(mode == 3):
                modethis += str(table3[tablech.index(i)])
            else:
                modethis += str(table4[tablech.index(i)])
            modethis += "."
        res += "\n\n"
        modethis = modethis[:-1]
    
    if(mode == 3):
        tar = url3_1.replace("ID",str(id))
        tar = tar.replace("TIME",str(int(time.time())))
        tar = tar.replace("26.25.24.23.22.21",modethis)
    else:
        tar = url4_1.replace("ID",str(id))
        tar = tar.replace("TIME",str(int(time.time())))
        tar = tar.replace("16.12.9.15.11.8",modethis)

    r = requests.get(tar)
    res1 = json.loads(r.text)

    if(res1["level"]["id"] > 20000):
        res1["level"]["id"] -= 10000
    if(res1["max_level"]["id"] > 20000):
        res1["max_level"]["id"] -= 10000


    res += "记录等级: " + ranktable[str(res1["level"]["id"])] + " "
    if(str(res1["level"]["id"])[2] == "7"):
        res += str((res1["level"]["score"] + res1["level"]["delta"])/100) + "/" 
    else:
        res += str(res1["level"]["score"] + res1["level"]["delta"]) + "/" 
    res += rankptMax[str(res1["level"]["id"])] + "pt\n"
    
    res += "历史最高: " + ranktable[str(res1["max_level"]["id"])] + " " 
    if(str(res1["max_level"]["id"])[2] == "7"):
        res += str((res1["max_level"]["score"] + res1["max_level"]["delta"])/100) + "/" 
    else:
        res += str(res1["max_level"]["score"] + res1["max_level"]["delta"]) + "/" 
    res += rankptMax[str(res1["max_level"]["id"])] + "pt\n"
    
    res += "对局场数: " + str(res1["count"]) + "场\n\n"

    res += "平均顺位: " + str(round(res1["avg_rank"],3)) + "\n"
    res += "一位率:   " + str(round(res1["rank_rates"][0]*100,2)) + "%\n"
    res += "二位率:   " + str(round(res1["rank_rates"][1]*100,2)) + "%\n"
    res += "三位率:   " + str(round(res1["rank_rates"][2]*100,2)) + "%\n"
    if(mode == 4):
        res += "四位率:   " + str(round(res1["rank_rates"][3]*100,2)) + "%\n\n"

    if(mode == 3):
        tar2 = url3_2.replace("ID",str(id))
        tar2 = tar2.replace("TIME",str(int(time.time())))
        tar2 = tar2.replace("26.25.24.23.22.21",modethis)
    else:
        tar2 = url4_2.replace("ID",str(id))
        tar2 = tar2.replace("TIME",str(int(time.time())))
        tar2 = tar2.replace("16.12.9.15.11.8",modethis)
    r2 = requests.get(tar2)
    res2 = json.loads(r2.text)

    res += "立直率:   " + str(round(res2["立直率"]*100,2)) + "%\n"
    res += "副露率:   " + str(round(res2["副露率"]*100,2)) + "%\n" 
    res += "和牌率:   " + str(round(res2["和牌率"]*100,2)) + "%\n" 
    res += "放铳率:   " + str(round(res2["放铳率"]*100,2)) + "%\n" 
    res += "默听率:   " + str(round(res2["默听率"]*100,2)) + "%\n"
    res += "自摸率:   " + str(round(res2["自摸率"]*100,2)) + "%\n"  

    return res
