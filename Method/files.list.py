# ファイル一覧取得
from openai import OpenAI

#client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client = OpenAI()
response = client.files.list()
print("ファイル一覧:", [file.id for file in response.data])
