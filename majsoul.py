#!/usr/bin/env python
# coding: utf-8

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import re
import datetime
import requests
import json
from bs4 import BeautifulSoup


url1 = "https://ak-data-1.sapk.ch/api/v2/pl4/search_player/name?limit=20"
url2 = "https://amae-koromo.sapk.ch/player/00000000/16.15.12.11.9.8"
url3 = "https://ikeda.sapk.ch/player/00000000/26.25.24.23.22.21"

l = [["Current rank","Current rk points","Recorded matches"],["Average rank","Call rate","Riichi rate"],["Win rate","Deal-in rate","Dama rate","Tsumo rate","Busting rate"]]
lch = [["记录等级", "记录分数", "记录场数"],["平均顺位","副露率","立直率"],["和牌率", "放铳率", "默胡率", "自摸率" , "被飞率"]]
rnk = ["Ad","Ex","Ms","St","Cl"]
rnkCh = ["雀士","雀杰","雀豪","雀圣","魂天"]

tablech = ["王座","王座东","玉","玉东","金","金东"]
table4 = ["16","15","12","11","9","8"]
table3 = ["26","25","24","23","22","21"]

def getid(name,mode = 4):
    tar = url1.replace("name", name)
    if (mode == 3):
        tar = tar.replace("pl4","pl3")
    r = requests.get(tar)
    res = json.loads(r.text)

    if len(res) == 0:
        return None
    # 可能会有多个结果，这里就当只有一个了
    return res[0]['id']

def getinfo(id,table = [],mode = 4):
    if mode == 4:
        tar = url2.replace("00000000", str(id))
    else:
        tar = url3.replace("00000000", str(id))
    opt = Options()
    opt.add_argument('--headless')
    opt.add_argument('--no-sandbox')
    opt.add_argument('--disable-dev-shm-usage')
    opt.add_argument('--disable-gpu')
    s = Service(r"../chromedriver")
    #driver = webdriver.Chrome(executable_path = "E:\DesktopFiles\chromedriver.exe",options=opt)  # 参数添加
    driver = webdriver.Chrome(service = s,options = opt)
    driver.get(tar)
    time.sleep(1)

 
    if(table != []):
        availabletable = []
        searchtable = ""
        curr_url = driver.current_url
        while (curr_url.find("/")>=0):
            curr_url = curr_url[curr_url.find("/")+1:]
        while (1):
            if(curr_url.find(".")>=0):
                tt = curr_url[:curr_url.find(".")]
                curr_url = curr_url[curr_url.find(".")+1:]
                availabletable.append(tt)
            else:
                availabletable.append(tt)
                break
        for i in table:
            if (mode == 4):
                j = table4[tablech.index(i)]
            else :
                j = table3[tablech.index(i)]
            if(not(j in availabletable)):
                error = "没有找到在"
                if(mode == 4):
                    error += "<四麻>"
                else:
                    error += "<三麻>"
                error += ("["+i+"]的对战!\n试一试对这位玩家搜索")
                for k in availabletable:
                    if mode == 4:
                        error += (" [" + tablech[table4.index(k)] + "] ")
                    else:
                        error += (" [" + tablech[table3.index(k)] + "] ")
                break
            else:
                if (searchtable == ""):
                    searchtable += j
                else:
                    searchtable += ("."+j)
        if (error != ""):
            return ["",error]
        if(mode == 4):
            tar = url2.replace("00000000", str(id))
            tar = tar.replace("16.15.12.11.9.8",searchtable)
        else:
            tar = url3.replace("00000000", str(id))
            tar = tar.replace("26.25.24.23.22.21",searchtable)
        driver.get(tar)
        time.sleep(1)

    text = driver.page_source
    #print(driver.page_source)
    driver.close()
    #soup = BeautifulSoup(text, 'lxml')
    return [text,""]

#print(getinfo(getid('ygmsdr')))


def getdata(text, ask="和牌率"):
    print(ask)
    res = re.findall(ask+".*?p>", text)[0]
    res = res[30:]
    pos = res.find(">")+1
    return res[pos:len(res)-4]
    
def getrk(text, ask = 1):
    rk = ["1st","2nd","3rd","4th"]
    rkch = ["一位", "二位", "三位", "四位"]
    res = re.findall(rk[ask-1]+".*?n>", text)[1]
    pos = res.find(">", res.find(">")+1)
    return res[pos+1:len(res)-8]

def searchQueHun(name,mode=4):
    table = []
    if(name.find(" ")):
        listname = list(name)
        listname.reverse()
        reversename = ''.join(listname)
        index = len(name) - reversename.find(" ")
        test = name[index:]
        if (test.find("王座") or test.find("玉") or test.find("金")):
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

    res = name + "\n"
    id = getid(name,mode)
    if(id == None):
        return "没有查到呢~"
    [text,error] = getinfo(id,table,mode)
    if (error != ""):
        error = name + " " + error
        return error 
    for i,i1 in zip(l,lch):
        for j,j1 in zip(i,i1) :
            if j1 == "记录等级":
                res += str(j1)
                temp = getdata(text,j)
                for R1,R2 in zip(rnk,rnkCh):
                    if temp.find(R1) >= 0:
                        temp = temp.replace(R1,R2)
                        break
                res += (" "+temp+"\n")
            else:
                res += str(j1) +" " +  getdata(text, j) + "\n"
        res += "\n"
    match = ["一位率","二位率","三位率","四位率"]
    for i in range(1,mode+1):
        print(i)
        res = res + str(match[i-1]) + " "  + getrk(text, i) + "\n"
    return res

