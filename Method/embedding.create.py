# テキストを 数値ベクトルに変換する
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.embeddings.create(
    model="text-embedding-ada-002",
    input="スマートシティのメリットとは？"
)

# ベクトルデータを取得
embedding_vector = response.data[0].embedding
print(embedding_vector)
#print(response)