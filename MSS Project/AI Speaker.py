# TTS와 STT를 활용한 인공지능과 대화하기

import time
import os  # 프로그램 종료 방지용
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import threading  # 호출어 이후, 일정시간의 대기시간이 지나면 명령권한 회수

isCall = False  # 호출어가 명령된 상태인지 확인
power = True  # 스피커의 전원에 해당
r = sr.Recognizer()
# = sr.Microphone()  # 마이크에 해당


def listen(recognizer, audio):  # 음성 인식 (듣기 )
    try:
        text = recognizer.recognize_google(audio, language='ko')
        print("[User] " + text)
        answer(text)
    except sr.UnknownValueError:
        print("인식 실패")  # 음성 인식이 실패한 경우
        speak("잘 듣지 못했어요")
    except sr.RequestError as e:  # 네트워크 등의 이유로 연결이 제대로 안됐을경우 API Key 오류, 네트워크 단절 등
        print("요청 실패 : {0}".format(e))  # 에러형식 출력
    pass


def answer(input_text):  # 어떤 대답을 할것인지 정의
    global isCall, power
    answer_text = ''  # 컴퓨터가 대답할 말 key값이 들어갔다면 출력되도록
    if '안녕' in input_text:
        answer_text = "안녕하세요? 반갑습니다."
    elif '날씨' in input_text:
        answer_text = "오늘 서울 기온은 20도입니다. 맑은 하늘이 예상됩니다."
    elif '환율' in input_text:
        answer_text = "원 달러 환율은 1400원입니다."
    elif '고마워' in input_text:
        answer_text = "별 말씀을요."
    elif '종료' in input_text:
        answer_text = "다음에 또 만나요."
        isCall = False
        power = False
        # stop_listening(wait_for_stop=False)  # 더이상 듣지 않음
    elif '자비스' in input_text:
        answer_text = "부르셨나요?"
    else:
        answer_text = "잘 이해하지 못했어요."

    speak(answer_text)


def speak(text):  # 소리내어 읽기 (TTS)
    print('[인공지능] ' + text)  # 인공지응이 하는말 텍스트 출력
    file_name = 'voice.mp3'
    tts = gTTS(text=text, lang='ko')  # 한글로 저장
    tts.save(file_name)  # file_name으로 해당 mp3파일 저장
    playsound(file_name)  # 저장한 mp3파일을 읽어줌
    if os.path.exists(file_name):  # file_name 파일이 존재한다면
        os.remove(file_name)  # 실행 이후 mp3 파일 제거


def reset_mode():
    global isCall
    print("다시 시도하세요")
    isCall = False


# 스피커가 동작하는 공간
while True:
    print("program start!")
    with sr.Microphone() as source:  # 마이크에서 들리는 음성(source)을 listen을 통해 들음
        print('듣고 있어요')  # 잠깐의 대기 시간이 있으므로 확인용으로 텍스트 출력
        callName = r.listen(source)  # 마이크로부터 호출어 듣기
        text = 0  # 예외처리문 밖에서도 이용하기 위해
        # 호출어에 대한 예외처리
        try:
            # 구글 API 로 인식 (하루 50회만 허용)
            # 영어는 language = 'en-US
            text = r. recognize_google(callName, language='ko')  # 영어 음성으로 변환
            print(text)
        except sr.UnknownValueError:
            print("인식 실패")  # 음성 인식이 실패한 경우
        except sr.RequestError as e:  # 네트워크 등의 이유로 연결이 제대로 안됐을경우 API Key 오류, 네트워크 단절 등
            print("요청 실패 : {0}".format(e))  # 에러형식 출력

        if "자비스" in text:  # 음성이 키워드일때 명령을 할수있게 변경
            isCall = True
            speak("안녕하세요!")

            # 아무 명령을 하지 않더라도, 20초가 지나면 명령 권한 회수
            start_time = threading.Timer(20, reset_mode)  # 20초후 reset
            start_time.start()
        else:
            continue

    # 명령 권한이 있는 상태에서는 계속 명령을 받을 수 있음
    while isCall:
        with sr.Microphone() as source:
            command = r.listen(source)  # 마이크로부터 음성 듣기
            listen(r, command)

# 계속 귀를 열어둠 m(마이크)를 통해 듣다가 내가 정의한 listen함수 호출
# stop_listening = r.listen_in_background(m, listen)  # listen 함수 호출
