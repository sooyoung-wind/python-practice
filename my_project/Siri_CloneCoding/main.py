# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 12:37:49 2023

@author: Soo.Y
"""
from src.call_api import call_api
from src.search import my_search
from src.load_modules import load_all_modules
from src.brown_smog import call_smog
from src.weather import call_weather_info
from src.my_speech import MySpeech
from src.extracting_search_words import extracting_search_words
isLoding = load_all_modules()  # call all of modules


googlemaps_api_key = ""  # input your api key
chromedriver_path = ""  # input your path
airKorea_api_key = ""  # input your api key
my_path_api_key = "../../env/data.env"  # input your api key file path

if len(googlemaps_api_key) == 0:
    googlemaps_api_key = call_api('googlemaps_api_key', my_path_api_key)
if len(chromedriver_path) == 0:
    chromedriver_path = call_api('chromedriver_path', my_path_api_key)
if len(airKorea_api_key) == 0:
    airKorea_api_key = call_api('airKorea_api_key', my_path_api_key)


if isLoding == True:
    print("=================================")
    print("시스템 로드를 완료했습니다.")
    print("=================================")
    isDoing = True
else:
    print("=================================")
    print("시스템 로드를 완료하지 못했습니다.")
    print("=================================")
    isDoing = False

# 유저 정보 입력

siri = MySpeech()
siri.speak()
keyword = "시리"
conversation_active = False

while isDoing:
    # stt tts 구현
    siri.voice_to_text()

    if keyword in siri.text:
        print('호출 완료')
        siri.text = "찾으셨습니까? 제가 무엇을 할까요?"
        siri.speak()
        siri.voice_to_text()

        if "구글" in siri.text:
            search_query = extracting_search_words(siri.text)
            full_url = "https://www.google.com/search?q=" + search_query
            if hasattr(siri, 'driver'):
                my_search(full_url, siri)
            else:
                siri.driver = my_search(full_url, siri)

        if "네이버" in siri.text:
            search_query = extracting_search_words(siri.text)
            full_url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=" + search_query
            if hasattr(siri, 'driver'):
                my_search(full_url, siri)
            else:
                siri.driver = my_search(full_url, siri)

        if "미세먼지" in siri.text:
            location_name = extracting_search_words(siri.text)
            call_smog(location_name, airKorea_api_key, siri)
        if "날씨" in siri.text:
            location_name = extracting_search_words(siri.text)
            call_weather_info(location_name, googlemaps_api_key, siri)
        if "기능" in siri.text:
            siri.text = "현재 구현된 기능은 검색기능, 날씨, 미세먼지 조회가 있습니다."
            siri.speak()

    if "종료" in siri.text:
        siri.text = "종료합니다."
        siri.speak()
        break
