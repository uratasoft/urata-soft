import os
import speech_recognition as sr
import pyttsx3
from openai import OpenAI

# 音声を録音してテキストに変換
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("質問をどうぞ！")
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio, language="ja-JP")
    except:
        return "すみません、うまく聞き取れませんでした。"

# ChatGPTに送信して返事をもらう
def ask_chatgpt(text):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": text}]
    )
    return response.choices[0].message.content

# AIの返事を声に出す
def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()

# すべてをつなげる
def talk_with_bot():
    question = listen()
    print("あなた：", question)
    answer = ask_chatgpt(question)
    print("Bot：", answer)
    speak(answer)

if __name__ == "__main__":
    talk_with_bot()