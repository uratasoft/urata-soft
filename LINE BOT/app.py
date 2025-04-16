from flask import Flask, request, abort
import json
import requests
from openai import OpenAI

app = Flask(__name__)

# 🔐 LINEのチャネルアクセストークンとChatGPTのAPIキーを設定（環境変数管理が推奨）
LINE_ACCESS_TOKEN = "5hgsQeZHs+6xHD+mJ0q4r7jR9s6qjl7hSecxaB1Rgj+v/RUfHqdGreNBxXeFcTOCmnyQPlgwOJmZEiHrfCjk46vArUS/U0kIUDsH3rTqpuqQl4tPocznQHs8I1UG+YXP9u6n6E7gHUaXPsogMGUoIQdB04t89/1O/w1cDnyilFU="
#client = OpenAI(api_key="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")

# 🤖 ChatGPTとやり取りする関数（シンプルなプロンプト処理）

def chat_with_gpt(message):
    client = OpenAI(api_key="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")
    message ="今日は休みです"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message}],
        max_tokens=50
    )
    return response.choices[0].message.content.strip()

# 🌐 Webhookのエントリーポイント（LINEからのPOSTリクエストを受信）
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("受信データ:", data)  # デバッグ用に受け取った内容を出力

    # ✅ Webhook検証リクエスト対策（"events" フィールドがない場合）
    if not data.get("events"):
        return "NO EVENTS", 200

    try:
        # 📩 ユーザーのメッセージと返信用トークンを取得
        user_message = data["events"][0]["message"]["text"]
        reply_token = data["events"][0]["replyToken"]

        # 💬 ChatGPTからの応答を生成
        response_text = chat_with_gpt(user_message)

        # 📨 LINEに返信を送るためのヘッダーとボディを準備
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
        }

        body = {
            "replyToken": reply_token,
            "messages": [{
                "type": "text",
                "text": response_text
            }]
        }

        # 🚀 LINEのMessaging APIで応答を送信
        requests.post(
            "https://api.line.me/v2/bot/message/reply",
            headers=headers,
            data=json.dumps(body)
        )

    except Exception as e:
        print("エラー:", e)  # 開発時のエラーログ
        return "ERROR", 200  # LINE側に200を返して再送を防止

    return "OK", 200

# 🖥 Flaskアプリの起動（WSLやngrok経由でもアクセス可能にする設定）
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
