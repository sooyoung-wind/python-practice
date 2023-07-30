# -*- coding: utf-8 -*-
"""
Created on Sun Jul 30 21:08:31 2023

@author: Soo.Y
"""
import sys
my_args = sys.argv[1]
my_id = my_args.split(';')[0]
my_pw = my_args.split(';')[1]

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

service = Service(executable_path=r"D:\Dev_folder\chromedriver-win64\chromedriver.exe")
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service = service, options=options)
url = 'https://www.instagram.com'
driver.get(url)


def login(my_id, my_pw):
    input_id = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input')
    input_id.send_keys(my_id)
    input_pw = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(my_pw)
    input_wd = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button').click()

time.sleep(3)
login(my_id, my_pw)


# serach
time.sleep(3)
hashtag = "강아지"
url = f"https://www.instagram.com/explore/tags/{hashtag}/"
driver.get(url)

# scroll
time.sleep(3)
for _ in range(5):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)



