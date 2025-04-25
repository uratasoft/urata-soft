import os
import speech_recognition as sr
import requests
import winsound
import json
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

# AIの返事をVOICEVOXでしゃべらせる
def speak(text, speaker=1):  # speaker=1 は「ずんだもん」
    try:
        query = requests.post(
            "http://127.0.0.1:50021/audio_query",
            params={"text": text, "speaker": speaker}
        ).json()

        synthesis = requests.post(
            "http://127.0.0.1:50021/synthesis",
            headers={"Content-Type": "application/json"},
            params={"speaker": speaker},
            data=json.dumps(query)
        )
        with open("voicevox_output.wav", "wb") as f:
            f.write(synthesis.content)

        #os.system("start voicevox_output.wav")  # Windows用
        winsound.PlaySound("voicevox_output.wav", winsound.SND_FILENAME)
    except Exception as e:
        print("VOICEVOXでエラーが発生しました：", e)

# すべてをつなげる
def talk_with_bot():
    question = listen()
    print("あなた：", question)
    answer = ask_chatgpt(question)
    print("Bot：", answer)
    speak(answer)

if __name__ == "__main__":
    talk_with_bot()
