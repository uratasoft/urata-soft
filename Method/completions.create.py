# 単純なテキスト補完を行う。
from openai import OpenAI
client = OpenAI()

response=client.completions.create(
  model="gpt-3.5-turbo-instruct",
  prompt="Say this is a test",
  max_tokens=7,
  temperature=0
)
print(response.choices[0].text)