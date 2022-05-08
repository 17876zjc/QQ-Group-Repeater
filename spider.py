#!/usr/bin/env python
# coding: utf-8

# In[41]:


from selenium import webdriver
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time
import re
import datetime
import requests
import json
from bs4 import BeautifulSoup
import random


# In[32]:


tar = 'https://s.mahjong.pub/#/quotation/'
opt = Options()
opt.add_argument('--headless')
opt.add_argument('--no-sandbox')
opt.add_argument('--disable-dev-shm-usage')
opt.add_argument('--disable-gpu')
driver = webdriver.Chrome(executable_path = r"../chromedriver",options=opt)  # 参数添加
driver.get('https://s.mahjong.pub/#/quotation/')
driver.current_url
time.sleep(2)


# In[53]:


def getallpic(text):
    l = re.findall(r'(<a data-src="https://.*?g")',text)
    for i in range(len(l)):
        l[i] = l[i][13:-1]
    return l

def turnpages(num):
    global driver
    button = driver.find_elements_by_xpath("//*/input[@value='第%d頁']" % num)[0]
    button.click()
    time.sleep(1)
    
pages = re.findall("(第\d*頁)", driver.page_source)  

print("Pages:\n")
print(pages)

maxpages = int(pages[-1][1:4])
print(maxpages)


# In[56]:


def getapic():
    global maxpages
    global driver
    page = random.randint(0, maxpages)
    turnpages(page)
    pic = random.choice(getallpic(driver.page_source))
    return pic


