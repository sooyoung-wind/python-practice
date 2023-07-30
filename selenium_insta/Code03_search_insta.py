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

time.sleep(5)
input_id = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input')
input_id.send_keys(my_id)
input_pw = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(my_pw)
input_wd = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button').click()

# serach
url = "https://.instagram.com/explore/tage/나비"


