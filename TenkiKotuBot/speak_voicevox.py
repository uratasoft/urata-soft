import requests
import json
import os

def speak_with_voicevox(text, speaker=1):  # speaker=1 は「ずんだもん」
    # クエリ生成
    query = requests.post(
        "http://127.0.0.1:50021/audio_query",
        params={"text": text, "speaker": speaker}
    ).json()

    # 音声合成
    audio = requests.post(
        "http://127.0.0.1:50021/synthesis",
        headers={"Content-Type": "application/json"},
        params={"speaker": speaker},
        data=json.dumps(query)
    ).content

    # ファイル保存＆再生
    with open("voicevox_output.wav", "wb") as f:
        f.write(audio)
    os.system("start voicevox_output.wav")  # Windowsの場合

if __name__ == "__main__":
    speak_with_voicevox("こんにちは！私がずんだもんです！")
