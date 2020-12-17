from pymongo import MongoClient
from bson.objectid import ObjectId

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

import os
import wget
import time
import json
import pprint

mongodb_host = os.environ.get('MONGO_HOST', 'localhost')
mongodb_port = int(os.environ.get('MONGO_PORT', '27017'))
client = MongoClient(mongodb_host, mongodb_port)   
db = client.scraping

def ScrapData():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome("./chromedriver", options=chrome_options)

    driver.get("https://www.youtube.com/feed/trending")

    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
    match=False
    while(match==False):
        lastCount = lenOfPage
        time.sleep(2)
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
        if lastCount==lenOfPage:
            match=True

    contents = []
    links = driver.find_elements_by_tag_name('a')
    for link in links:
        post = link.get_attribute('href')
        if post is not None:
            if '/watch' in post:
                title = link.get_attribute('title')
                contents.append({"url" : post, "title" :title})

    # for i in range(len(contents)):
    #     if i%2==1:
    #         print(contents[i])

    return contents


def CreateData(data):
    try:
        for i in range(len(data)):
            if i%2==1:
                db.youtube.insert(data[i])
    except:
        print("Cannot insert data")

def ReadData():

    instagram = db.youtube.find()

    result =[]
    for i in instagram:
        result.append(i)

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(result)

# menjalankan scraping 
data = ScrapData()

# menyimpan data
CreateData(data)

# memanggil data
ReadData()
