import requests
import json

# 날씨/대기상태라는 하나의 큰 목적을 공유하고 있어서 클래스로 만들어보았는데,
# 지금 정도의 함수만 있다면 굳이 하나의 클래스로 만들 필요는 없어보임
class WeatherApi:
    def __init__(self, api_key):
        self.locations = {'서울':{'latitude': 37.56, 'longitude': 126.97},
                    '부산':{'latitude': 35.10, 'longitude': 129.03}}
        self.service_key = api_key

    def get_weather(self, location):
        try:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={self.locations[location]['latitude']}&longitude={self.locations[location]['latitude']}&current_weather=true&timezone=auto"
            response = requests.get(url)
            json_data = json.loads(response.text)
            return f"{json_data['current_weather']['temperature']}°C"
        except KeyError:
            # 각 함수마다의 예외처리 또한 필수적으로 해줘야함 (없는 지역이 인자로 들어온다면?, 요청이 실패한다면? 등 모든 경우에 대해 전부 예외처리 필요)
            # 혹은 공통적으로 사용할 validate_location 함수를 따로 만들어서 사용해도 괜찮을 듯
            return '없는 지역'

    def get_airinfo(self, location):
        try: 
            params = {
                'serviceKey': self.service_key,
                'returnType': 'json',
                'numOfRows': '100',
                'pageNo': '1',
                'sidoName': location,
                'ver': '1.0',
            }
            response = requests.get('http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty', params=params)
            json_data = json.loads(response.text)
            airinfo_list = json_data['response']['body']['items']
            # 만약 stationName 도 인자로 받고, 필터링해서 결과를 보여주고 싶다면
            # airinfo = list(filter(lambda x: x['stationName'] == stationName, airinfo_list))
            return airinfo_list[0]['pm25Value']
        except IndexError:
            return '없는 지역'
        except KeyError:
            return '없는 지역'