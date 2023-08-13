from gtts import gTTS 
import playsound
import os

# 이 부분은 간단한 코드라서 따로 클래스화하지 않았음
def speak(text): 
	tts = gTTS(text=text, lang='ko') 
	tts.save('voice.mp3') 
	playsound.playsound('voice.mp3')
	os.remove('voice.mp3')