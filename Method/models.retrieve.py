# 特定モデルの詳細情報取得
from openai import OpenAI

#client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client = OpenAI()

response = client.models.retrieve("gpt-4-turbo")
print("GPT-4 Turboの詳細情報:", response)
