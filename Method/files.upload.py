# ファイルアップロード
from openai import OpenAI

#client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client = OpenAI()

with open("C:\\Users\\user\\anaconda3\\PythonAI\\KDP\\Method\\test.jsonl", "rb") as file:
    response = client.files.create(
        file=file,
        purpose="fine-tune"
    )
print("アップロードされたファイルID:", response.id)
