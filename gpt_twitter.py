import openai
import os

# 環境変数からOpenai APIキーを取得する
openai.aip_key = os.environ["OPENAI_API_KEY"]

# ChatGPTによるツイート作成関数
def make_tweet():
    request = "私はAIを研究する企業を経営しています。私に代わってTwitterに投稿するツイートを150以内で作成して下さい。\n\nツイート作成の際は以下の文章を参考にして下さい。\n\n"

    tweet1 = "例文1:私ChatGPTは浦田さんに代わってツイートしています。"

    tweet2 = "例文2:私のfacebook'https://www.facebook.com/UrataSoft'もよろしくお願いします。"

    content = request + tweet1 + tweet2

    response = openai.chat.completions.create(
        
        model="gpt-3.5-turbo",
        temperature=0,
        messages=[
            {"role": "user", "content": content},
        ],
    )

    return response.choices[0].message.content
