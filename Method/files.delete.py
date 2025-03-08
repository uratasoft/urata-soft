# ファイルデリーと
from openai import OpenAI

#client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client = OpenAI()

file_id = "file-Ad2aQJTLFiSSHGwLkt9C4k"
response = client.files.delete(file_id)
print(f"ファイル {file_id} の削除結果:", response.deleted)
