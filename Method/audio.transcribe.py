# 音声ファイルをテキストに変換する
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 音声ファイルのパスを指定
audio_file_path = "C:\\Users\\user\\anaconda3\\PythonAI\\KDP\\Method\\dakaretai.mp3"

# 音声ファイルを開いてAPIに送信
with open(audio_file_path, "rb") as audio_file:
    response = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        response_format="text"  # 他に "json" も選択可能
    )

# 文字起こし結果を表示
print(response)
