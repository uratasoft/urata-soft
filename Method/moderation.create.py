# テキストの安全性をチェック し、不適切な内容を検出

import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.moderations.create(
    model="text-moderation-latest",
    input="殺人クラブ"
)

# テキストが危険かどうかを判定
is_flagged = response.results[0].flagged
print(f"このテキストは危険か？: {is_flagged}")