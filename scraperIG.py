from pymongo import MongoClient
from bson.objectid import ObjectId

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
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

instagram_user = "detikcom"

def ScrapData(instagram_user):

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome("./chromedriver", options=chrome_options)
    driver.get("https://www.instagram.com/{}".format(instagram_user))

    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
    match=False
    while(match==False):
        lastCount = lenOfPage
        time.sleep(3)
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
        if lastCount==lenOfPage:
            match=True

            # klik button Show More Post from {user}, belum bisa tereksekusi
            # element = driver.find_element_by_link_text("Show More Post from {}".format(instagram_user)) 
            # element.click() 

    posts = []
    links = driver.find_elements_by_tag_name('a')
    for link in links:
        post = link.get_attribute('href')
        if '/p/' in post:
            posts.append(post)
    
    return posts

def CreateData(data, ig_user):
    try:
        for i in range(len(data)):
            db.instagram.insert({"user" : ig_user, "post_url" : data[i]})
    except:
        print("Cannot insert data")

def ReadData():

    instagram = db.instagram.find()

    result =[]
    for i in instagram:
        result.append(i)

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(result)

# menjalankan scraping 
data = ScrapData(instagram_user)

# menyimpan data
CreateData(data, instagram_user)

# memanggil data
ReadData()

