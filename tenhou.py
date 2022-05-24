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

url1 = "https://nodocchi.moe/tenhoulog/#!&name="

def getinfo(id):
    tar = url1 + str(id)

    opt = Options()
    opt.add_argument('--headless')
    opt.add_argument('--no-sandbox')
    opt.add_argument('--disable-dev-shm-usage')
    opt.add_argument('--disable-gpu')
    opt.add_argument('--lang=zh_cn')
    #opt.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"')
    s = Service(r"../chromedriver")
    #s = Service(r"E:\DesktopFiles\chromedriver.exe")
    #driver = webdriver.Chrome(executable_path = "E:\DesktopFiles\chromedriver.exe",options=opt)  # 参数添加
    driver = webdriver.Chrome(service = s,options = opt)
    driver.get(tar)
    time.sleep(1)

    text = driver.page_source
    driver.quit()
    #return text
    if(re.findall("找不到指定的对局",text) != []):
        return "没有查到呢~"
    else:
        return(str(id) + "\n\n" + analy1(text) + "\n" + analy2(text) + "\n" + analy3(text) + "\n" + analy4(text))

def analy1(text):
    ans = ""
    res = re.findall(r"推定段位.*?段位排名",text)[0]

    r1 = re.findall(r"四麻.*?\dpt",res)[0]
    t1 = re.findall(r"\">.*?pt",r1)[0]
    ans += ("当前段位 "+t1[2:4]+" "+t1[9:])
    if(re.findall(r"新高",r1) != []):
        ans+=" ★"
    ans += "\n"

    r1 = re.findall(r"历史最高.*?\dpt",res)[0]
    t1 = re.findall(r"\">.*?pt",r1)[0]
    ans += ("历史最高 "+t1[2:4]+" "+t1[9:] + "\n")

    r1 = re.findall(r"推定R值.*?R\d\d\d\d",res)[0]
    ans += ("当前R值  "+r1[-5:])
    if(re.findall(r"新高",r1) != []):
        ans+=" ★"
    ans += "\n"

    r1 = re.findall(r'R\d\d\d\d.*?R\d\d\d\d',res)[0][-5:]
    ans+=("历史最高 "+r1+"\n")

    r1 = re.findall(r"段位战.*?战",res)[0]
    t1 = re.findall(r"\"\>.*?战",r1)[0]
    ans+=("对战次数 "+ t1[2:]+"\n")

    return(ans)

def analy2(text):
    ans = ""
    res = re.findall(r"推定安定段位.*?三麻",text)[0]

    r1 = re.findall(r"四麻.*?段位战",res)[0]
    t1 = re.findall(r"\"\>.*?\</",r1)[0]
    ans+=("推定安定段位 "+ t1[2:4] + t1[9:-2] + "\n")

    r1 = re.findall(r"预计.*?\<",res)[0]
    ans+=(r1[:-1]+"\n")
    
    return(ans)

def analy3(text):
    ans = ""
    res = re.findall(r"对战顺位统计.*?三麻",text)[0]

    for i in range(1,5):
        r1 = re.findall(str(i)+r"位.*?战",res)[0]
        t1 = re.findall(r"\">.*?战",r1)[0]
        ans+=(str(i)+"位 "+t1[2:]+" ")

        r1 = re.findall(str(i)+r"位.*?‰",res)[0]
        t1 = re.findall(r"战.*?‰",r1)[0]
        t2 = re.findall(r"\">.*?‰",t1)[0]
        ans+= (t2[2:]+"\n")

    return(ans)

def analy4(text):
    ans = ""
    res = re.findall(r"对战结果统计.*?三麻",text)[0]

    r1 = re.findall(r"平顺.*?通得",res)[0]
    t1 = re.findall(r"\">.*?<",r1)[0]
    ans += ("平均顺位 "+t1[2:-1])

    return(ans)
