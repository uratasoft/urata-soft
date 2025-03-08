# 
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

image_path = "input.png"
mask_path = "mask.png"

with open(image_path, "rb") as image, open(mask_path, "rb") as mask:
    response = client.images.edit(
        model="dall-e-3",
        image=image,
        mask=mask,
        prompt="都市の背景を夜景に変更してください。",
        n=1,
        size="1024x1024"
    )

image_url = response.data[0].url
print("編集された画像のURL:", image_url)
