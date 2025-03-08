# 利用可能なモデル一覧取得
import os
from openai import OpenAI

#client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client = OpenAI()

response = client.models.list()
print("利用可能なモデル一覧:", [model.id for model in response.data])
