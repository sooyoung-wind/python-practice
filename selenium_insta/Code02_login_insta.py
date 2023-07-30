# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 18:28:12 2023

@author: Soo.Y
"""
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

service = Service(executable_path=r"D:\Dev_folder\chromedriver-win64\chromedriver.exe")
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service = service, options=options)
url = 'https://www.naver.com'
url = 'https://www.instagram.com'
driver.get(url)

my_id = "paulham98@naver.com" ### os.env
my_pw = "skull034456!"

time.sleep(5)
input_id = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input')
input_id.send_keys(my_id)
input_pw = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(my_pw)
input_wd = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button').click()
