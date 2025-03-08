#画像のバリデーションを作成
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

with open("C:\\Users\\user\\anaconda3\\PythonAI\\KDP\\Method\\T.Urata.JPG", "rb") as image:
    response = client.images.generate(
        model="dall-e-3",
        #image=image, # images.variation用
        prompt="この画像を基本に多少イケメン風にして下さい",
        n=1,
        size="1024x1024"
    )

image_url = response.data[0].url
print("バリエーション画像のURL:", image_url)
