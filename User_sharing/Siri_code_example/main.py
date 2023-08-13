from assistant import Assistant

# 실행하는 예시를 쉽게 보여드리고자 파일 자체를 분리했는데,
# 클래스 파일에 main함수 형태로 아래 코드를 넣어놓고 sysarg 형태로 인자 값을 받게 만들어도 무방
instance = Assistant('이름', weather_api_key='키', game_api_key='키')
instance.start()