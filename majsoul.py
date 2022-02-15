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
url2 = "https://amae-koromo.sapk.ch/player/00000000/16.12.11.9.8"

def getid(name):
    tar = url1.replace("name", name)
    r = requests.get(tar)
    res = json.loads(r.text)
    if len(res) == 0:
        return None
    # 可能会有多个结果，这里就当只有一个了
    return res[0]['id']

def getinfo(id):
    tar = url2.replace("00000000", str(id))
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
    text = driver.page_source
    #print(driver.page_source)
    driver.close()
    #soup = BeautifulSoup(text, 'lxml')
    return text

#print(getinfo(getid('ygmsdr')))


def getdata(text, ask="和牌率"):
    print(ask)
    temp = re.findall(ask+".*?p>", text)
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

l = [["Current rank","Current rk points","Recorded matches"],["Average rank","Call rate","Riichi rate"],["Win rate","Deal-in rate","Dama rate","Tsumo rate","Busting rate"]]
lch = [["记录等级", "记录分数", "记录场数"],["平均顺位","副露率","立直率"],["和牌率", "放铳率", "默胡率", "自摸率" , "被飞率"]]
rnk = ["Ad","Ex","Ms","St","Cl"]
rnkCh = ["雀士","雀杰","雀豪","雀圣","魂天"]


def searchQueHun(name):
    res = name + "\n"
    id = getid(name)
    if(id == None):
        return "没有查到呢~"
    text = getinfo(id)
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
    for i in range(1,5):
        print(i)
        res = res + str(match[i-1]) + " "  + getrk(text, i) + "\n"
    return res

