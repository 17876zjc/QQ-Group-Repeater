from numpy import double

from sympy import false, true
from util import load_json
import requests
import json
import time
import urllib.parse

url = "https://nodocchi.moe/api/listuser.php?name="
urlrank = "https://nodocchi.moe/s/ugr/***.js"

levelmap = {
    0: {'name': '新人', 'initscore': 0, 'maxscore': 20, 'haslower': False, 'losescore': [0,0]},
    1: {'name': '9级', 'initscore': 0, 'maxscore': 20, 'haslower': False, 'losescore': [0,0]},
    2: {'name': '8级', 'initscore': 0, 'maxscore': 20, 'haslower': False, 'losescore': [0,0]},
    3: {'name': '7级', 'initscore': 0, 'maxscore': 20, 'haslower': False, 'losescore': [0,0]},
    4: {'name': '6级', 'initscore': 0, 'maxscore': 40, 'haslower': False, 'losescore': [0,0]},
    5: {'name': '5级', 'initscore': 0, 'maxscore': 60, 'haslower': False, 'losescore': [0,0]},
    6: {'name': '4级', 'initscore': 0, 'maxscore': 80, 'haslower': False, 'losescore': [0,0]},
    7: {'name': '3级', 'initscore': 0, 'maxscore': 100, 'haslower': False, 'losescore': [0,0]},
    8: {'name': '2级', 'initscore': 0, 'maxscore': 100, 'haslower': False, 'losescore': [10,15]},
    9: {'name': '1级', 'initscore': 0, 'maxscore': 100, 'haslower': False, 'losescore': [20,30]},
    10: {'name': '初段', 'initscore': 200, 'maxscore': 400, 'haslower': True, 'losescore': [30,45]},
    11: {'name': '二段', 'initscore': 400, 'maxscore': 800, 'haslower': True, 'losescore': [40,60]},
    12: {'name': '三段', 'initscore': 600, 'maxscore': 1200, 'haslower': True, 'losescore': [50,75]},
    13: {'name': '四段', 'initscore': 800, 'maxscore': 1600, 'haslower': True, 'losescore': [60,90]},
    14: {'name': '五段', 'initscore': 1000, 'maxscore': 2000, 'haslower': True, 'losescore': [70,105]},
    15: {'name': '六段', 'initscore': 1200, 'maxscore': 2400, 'haslower': True, 'losescore': [80,120]},
    16: {'name': '七段', 'initscore': 1400, 'maxscore': 2800, 'haslower': True, 'losescore': [90,135]},
    17: {'name': '八段', 'initscore': 1600, 'maxscore': 3200, 'haslower': True, 'losescore': [100,150]},
    18: {'name': '九段', 'initscore': 1800, 'maxscore': 3600, 'haslower': True, 'losescore': [110,165]},
    19: {'name': '十段', 'initscore': 2000, 'maxscore': 4000, 'haslower': True, 'losescore': [120,180]},
    20: {'name': '天凤', 'initscore': 2200, 'maxscore': 100000, 'haslower': False, 'losescore': [0,0]}
}
ptchange = {
    '4': [{
            '0': (20, 10, 0),
            '1': (40, 10, 0),
            '2': (50, 20, 0),
            '3': (60, 30, 0)
        },
        {
            '0': (30, 15, 0),
            '1': (60, 15, 0),
            '2': (75, 30, 0),
            '3': (90, 45, 0)
        }],
    'old4': {
        '0': (30, 0, 0),
        '1': (40, 10, 0),
        '2': (50, 20, 0),
        '3': (60, 30, 0)
    }
}

def getRank(list,name):
    currank = currpt = 0
    lasttime = thistime =  0
    for i in list:
        if lasttime == 0:
            lasttime = thistime = int(i['starttime'])
        else:
            thistime = int(i['starttime'])
            if (thistime-lasttime) > 60*60*24*180 and currank < 16:
                currank = currpt = 0
            lasttime = thistime
        if((i['sctype'] == "b" or i['sctype'] == "c") and i['playernum'] == "4"):
            lv = int(i['playerlevel'])
            len_ = int(i['playlength'])
            pt = 0
            for j in range(1,5):
                if i['player'+str(j)] == str(name):
                    pt = double(i['player'+str(j)+'ptr'])
                    break
            rank = 1
            for j in range(1,5):
                if double(i['player'+str(j)+'ptr']) > pt:
                    rank = rank+1
            ptDelta = 0
            flag = true
            if(lv == 0 and len_ == 1):
                t = time.localtime(thistime)
                if t.tm_year<=2017:
                    if t.tm_mon<=10:
                        if t.tm_mday <= 22 or (t.tm_mday == 23 and t.tm_hour <23):
                            flag = false
                            if rank == 1:
                                ptDelta = 30
                            elif rank == 2 or ptDelta == 3:
                                ptDelta = 0
                            else:
                                ptDelta = 0 - levelmap[currank]['losescore'][len_-1]
            if flag == true:
                if rank == 4:
                    ptDelta = 0 - levelmap[currank]['losescore'][len_-1]
                else:
                    ptDelta = ptchange['4'][len_-1][str(lv)][rank-1]
            #print(ptDelta)
            currpt = currpt + ptDelta
            if(currpt >= levelmap[currank]['maxscore']):
                currank = currank + 1
                currpt = levelmap[currank]['initscore']
            elif(currpt < 0 ):
                if(levelmap[currank]['haslower'] == True):
                    currank = currank - 1
                    currpt = levelmap[currank]['initscore']
                else:
                    currpt = 0
    if currank==20:
        currpt = 2200
    return (currank,currpt)


def getinfo(name):
    maxrank = currank = 0
    maxpt = currpt = levelmap[currank]['initscore']
    position = [0,0,0,0]
    tar = url+urllib.parse.quote(str(name))
    r = requests.get(tar)
    res = json.loads(r.text)
    if(res == False):
        return "没有找到该玩家!"
    lasttime = thistime =  0

    for i in res['list']:
        if lasttime == 0:
            lasttime = thistime = int(i['starttime'])
        else:
            thistime = int(i['starttime'])
            if (thistime-lasttime) > 60*60*24*180 and currank < 16:
                maxrank = maxpt = currank = currpt = 0
                position = [0,0,0,0]
            lasttime = thistime
        if((i['sctype'] == "b" or i['sctype'] == "c") and i['playernum'] == "4"):
            lv = int(i['playerlevel'])
            len_ = int(i['playlength'])
            pt = 0
            for j in range(1,5):
                if i['player'+str(j)] == str(name):
                    pt = double(i['player'+str(j)+'ptr'])
                    break
            rank = 1
            for j in range(1,5):
                if double(i['player'+str(j)+'ptr']) > pt:
                    rank = rank+1
            position[rank-1] = position[rank-1] + 1
            ptDelta = 0
            flag = true
            if(lv == 0 and len_ == 1):
                t = time.localtime(thistime)
                #print(t)
                if thistime < 1508857200 :
                    flag = false
                    if rank == 1:
                        ptDelta = 30
                    elif rank == 2 or rank == 3:
                        ptDelta = 0
                    else:
                        ptDelta = 0 - levelmap[currank]['losescore'][len_-1]
            if flag == true:
                if rank == 4:
                    ptDelta = 0 - levelmap[currank]['losescore'][len_-1]
                else:
                    ptDelta = ptchange['4'][len_-1][str(lv)][rank-1]
            #print(ptDelta)
            currpt = currpt + ptDelta
            if(currpt >= levelmap[currank]['maxscore']):
                currank = currank + 1
                currpt = levelmap[currank]['initscore']
                #print("\t升段至 "+levelmap[currank]['name'])
            elif(currpt < 0 ):
                if(levelmap[currank]['haslower'] == True):
                    currank = currank - 1
                    currpt = levelmap[currank]['initscore']
                    #print("\t降段至 "+levelmap[currank]['name'])
                else:
                    currpt = 0
            if currank > maxrank or (currank == maxrank and currpt > maxpt):
                maxrank = currank
                maxpt = currpt 
    if currank==20:
        maxpt = currpt = 2200
        maxrank = 20


    recentrank = ""
    recordlen = len(res['list'])
    count = -1
    while(len(recentrank)<10):
        if(count + recordlen < 0):
            break
        i = res['list'][count]
        count = count - 1
        if(not((i['sctype'] == "b" or i['sctype'] == "c") and i['playernum'] == "4")):
            continue
        pt = 0
        for j in range(1,5):
            if i['player'+str(j)] == str(name):
                pt = double(i['player'+str(j)+'ptr'])
                break
        rank = 1
        for j in range(1,5):
            if double(i['player'+str(j)+'ptr']) > pt:
                rank = rank+1
        recentrank += str(rank)
        


    ans = (name+"\n当前段位: "+levelmap[currank]['name']+" "+str(currpt)+"pt")
    if (currank == maxrank and currpt == maxpt):
        ans = ans + "★"
    ans = ans + ("\n历史最高: "+levelmap[maxrank]['name']+" "+str(maxpt)+"pt")

    if ("4" in res["rate"]):
        ans = ans+("\n推定R值: R"+str(res["rate"]["4"]))

    tarrank = str(urlrank).replace("***",name)
    r1 = requests.get(tarrank)
    res1 = json.loads(r1.text)
    if "4" in res1:
        ans = ans+"\n段位排名: "+str(res1['4']['graderank'])+" 名"

    ans = ans + "\n                --------->最新"
    ans = ans + "\n最近战绩: ["+recentrank[::-1]+"]" 

    gamenum = position[0]+position[1]+position[2]+position[3]
    ans = ans+"\n\n总计对战: "+str(gamenum)+ " 场\n"
    ans = ans+"一位: "+str(position[0])+ " 场\t"+ str(round(float(position[0]/gamenum)*100,2))+"%\n"
    ans = ans+"二位: "+str(position[1])+ " 场\t"+ str(round(float(position[1]/gamenum)*100,2))+"%\n"
    ans = ans+"三位: "+str(position[2])+ " 场\t"+ str(round(float(position[2]/gamenum)*100,2))+"%\n"
    ans = ans+"四位: "+str(position[3])+ " 场\t"+ str(round(float(position[3]/gamenum)*100,2))+"%\n"
    ans = ans+"平均顺位: "+str(round((position[0]*1+position[1]*2+position[2]*3+position[3]*4)/gamenum,3))

    return ans