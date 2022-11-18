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



# In[53]:


def getallpic(text):
    l = re.findall(r'(<a data-src="https://.*?g")',text)
    for i in range(len(l)):
        l[i] = l[i][13:-1]
    return l

    
    


#print("Pages:\n")
#print(pages)


#print(maxpages)


# In[56]:


def getapic():

    tar = 'https://s.r-mj.com/#/quotation/'
    opt = Options()
    opt.add_argument('--headless')
    opt.add_argument('--no-sandbox')
    opt.add_argument('--disable-dev-shm-usage')
    opt.add_argument('--disable-gpu')
    driver = webdriver.Chrome(executable_path = r"/root/QQ/chromedriver",options=opt)  # 参数添加
    driver.get(tar)
    #driver.current_url
    time.sleep(2)

    pages = re.findall("(第\d*頁)", driver.page_source)  

    maxpages = int(pages[-1][1:4])

    page = random.randint(0, maxpages)
    
    button = driver.find_elements_by_xpath("//*/input[@value='第%d頁']" % page)[0]
    button.click()
    time.sleep(1)

    pic = random.choice(getallpic(driver.page_source))

    driver.quit()
    return pic


