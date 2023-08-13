import requests
import json
from tts import speak
from stt import SttEngine

class RelayGame:
    def __init__(self, api_key, turn=1, default_word='사과'):
        self.api_key = api_key
        self.turn = turn
        self.default_word = default_word
        self.previous_words = []
        self.stt_engine = SttEngine()

    def get_words(self, query, method):
        # request가 실패할 경우에 대비한 예외처리도 해주는 것이 맞음 (다만 네트워크와 관련된 부분이기도 하고, 코드가 너무 길어지는 것을 막고자 예제코드에서는 하지 않았음)
        headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
        response = requests.get(f'http://opendict.korean.go.kr/api/search?key={self.api_key}&req_type=json&q={query}&advanced=y&sort=popular&type1=word&method={method}&num=100&pos=1&type3=general', headers=headers)
        json_data = json.loads(response.text)
        return json_data['channel']['item']
    
    def validate_word(self, query):
        result = self.get_words(query, 'exact')
        return result != []
    
    def input_with_validation(self):
        while True:
            my_word = self.stt_engine.recognize()
            if my_word is None: # 아무 말도 안했으면, 따로 조건검사없이 다시 인식하도록
                continue # 다음 루프로
            elif len(my_word) < 2: # 각 조건문 마다 함수 형태로 만든 후에, 딕셔너리 형태로 만들어서 elif 문의 중첩을 제거할 수는 있음
                speak('2자 이상 말해주세요.')
            elif self.previous_words != [] and my_word[0] != self.previous_words[-1][-1]:
                speak('끝말을 잇지 않았습니다.')
            elif my_word in self.previous_words:
                speak('이미 나온 단어입니다.')
            elif not self.validate_word(my_word):
                speak('없는 단어입니다.')
            else:
                return my_word
    
    def get_next_word(self, query):
        words = self.get_words(query, 'start')
        for word in words:
            if len(word['word']) < 2:
                continue
            if word['word'] not in self.previous_words:
                return word['word']
        return None # 위에서 return 되지 않았다면 더 이상 조건에 맞는 단어가 없다는 뜻이므로,
    
    def start(self):
        while True:
            if self.turn == 1: # 내 차례
                current_word = self.input_with_validation() 
            else: # 컴퓨터 차례
                previous_word = self.previous_words[-1] if self.previous_words else self.default_word
                current_word = self.get_next_word(previous_word[-1])
                speak(current_word) 
            self.previous_words.append(current_word) # 지금까지 나온 단어 리스트에 추가
            self.turn = not self.turn # 다음 턴