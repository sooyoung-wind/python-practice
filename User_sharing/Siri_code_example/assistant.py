from weather import WeatherApi
from game import RelayGame
from crawl import crawl_naver
from tts import speak
from stt import SttEngine

class Assistant:
    def __init__(self, name, weather_api_key, game_api_key):
        self.name = name
        self.stt_engine = SttEngine() # stt 엔진, api 등은 비서의 작동 방식 그 자체에 대한 코드는 아니므로 모듈 형태로 분리
        self.weather_api = WeatherApi(weather_api_key) # api key 때문에 해당 클래스 내부 코드를 수정하지 않아도 되도록, 객체 생성 시 api key 지정
        self.relay_game = RelayGame(game_api_key) # 마찬가지
        # 각 동작들은 1. 동작 실행 후에 대답이 필요한 경우 / 없는 경우 2. 동작 실행에 인자가 필요한 경우 / 없는 경우로 유형화할 수 있음 (총 4개의 유형)
        # 여기서 유형화를 정확히 해주어야, 밑에서 동작을 처리하는 함수가 제대로 추상화될 수 있음
        # 유형을 어떻게 나눴는지에 따라서, 형식이 더 간단해질 수 있을 것
        self.action_phrase = {'검색': {'type': 'act', 'need_args': True, 'msg': '검색하겠습니다', 'command': crawl_naver},
                            '날씨': {'type': 'speak', 'need_args': True, 'msg': '실시간 날씨 알려드릴게요', 'command': self.weather_api.get_weather},
                            '미세먼지': {'type': 'speak', 'need_args': True, 'msg': '실시간 미세먼지 알려드릴게요', 'command': self.weather_api.get_airinfo},
                            '게임': {'type': 'act', 'need_args': False, 'msg': '시작하겠습니다', 'command': self.relay_game.start}}
        self.error_phrase = {'type': None, 'need_args': None, 'msg': '다시 말씀해주세요.', 'command': None}
        # 이름을 불러서 준비된 상태인지
        self.is_ready = True

    # 사용자가 한 말을 두 개의 구문 (명령 / 명령에 필요한 인자) 으로 분석 (실제 서비스라면 여기서 nltk 를 쓰거나 nlp 관련 모델이 들어가겠지만..)
    def analyze_phrase(self, phrase):
        splited_phrase = phrase.split()
        action = splited_phrase[-1].strip()
        argument = ''.join(splited_phrase[:-1])
        return action, argument

    # 분석된 구문에 따라 해야할 행동을 찾고, 그에 따라 작동 
    def process_phrase(self, action, argument):
        payload = self.action_phrase.get(action, self.error_phrase)
        speak(payload['msg'])
        if not payload['type']: # 우리가 준비한 어떤 action에도 해당하지 않는다면 (type이 None이라면) 작동하지 않음
            return
        # if not return 문 때문에 아래는 payload['type'] 이 있는 경우에만 동작함 (사실상 if else 문과 같음)
        # need_args가 True인 경우 인자가 필요하므로 명시, 아닌 경우 명시하지 않고 함수 실행 (인자가 이상할 경우의 예외처리는 각 함수 안에서 진행)
        result = payload['command'](argument) if payload['need_args'] else payload['command']()
        # 대답이 필요한 동작이라면 대답까지 (이렇게 타입을 나누지 않고, command 함수 안에서 speak 를 사용해도 되지만, 재사용성을 고려해서 타입을 나누고 speak 코드를 분리했음)
        if payload['type'] == 'speak':
            speak(f"{result}입니다")

    # 메인 함수
    def start(self):
        while True:
            speech = self.stt_engine.recognize()
            if self.is_ready: # 이름을 불러서 준비된 상태라면
                if speech is None: # 명령할 때까지 루프하며 대기
                    continue
                action, argument = self.analyze_phrase(speech) # 명령 분석
                self.process_phrase(action, argument) # 분석 결과에 따라 동작
                self.is_ready = not self.is_ready # 동작했으니 다시 준비안된 상태로 돌아감
            elif speech == self.name: # 준비되지 않았고, 이름을 불렀다면
                self.is_ready = True # 준비 상태로
                speak('네 말씀하세요.')
            # 준비되지 않았고, 이름도 안불렀다면 아무것도 하지 않음