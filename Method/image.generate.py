# テキストから画像を生成する
import os
from openai import OpenAI

#client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client = OpenAI()

response = client.images.generate(
    model="dall-e-3",
    prompt="2035年千葉県流山市松ヶ丘スマートシティ高層ビル街の街並み、南柏駅も高架線上に存在する、地上40階建てのウラタビルの屋上にウラタとローマ字で書かれている、会社も学校も病院も高層ビルに存在する、ドローンの荷物集配所がある、南西には富士山が見える、30キロ南西にはスカイツリーが見える、自動運転用の高速道路が東京方面に延びている",
    size="1024x1024",
)

print(response.data[0].url)
