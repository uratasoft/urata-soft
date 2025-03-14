import requests
from flask import Flask, request

app = Flask(__name__)

# 🔹 Facebook の「ページアクセストークン」を設定（あなたのものに置き換えてください！）
PAGE_ACCESS_TOKEN = "EAAOhc6h5nBABOxTTixCeGLdvZBvU7ckBUJSIVwlBfmSZAfeonLm9y0NfoFrDArahJNZCm47JgiBrdIyRebdYlwckZCMRoPx4ZA2gvzOClsJ5GZCBZAjWAmYEshRje4SF3vx4BpR91qPDdHsOu3CHeWUijuRGXex8yXZAgsdEjBi3VqGdTsCXAK6D7A5ZCs8qxsSoO1GtAQK1OMp4LguRZBK9gxCnZAnGR34uEBF3aAKtnehDQYZD"  # ここにあなたのページアクセストークンを入力

def send_message(recipient_id, text):
    """Facebook Messenger に自動返信を送る"""
    url = f"https://graph.facebook.com/v19.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": text}
    }
    response = requests.post(url, json=payload, headers=headers)
    print("📩 送信結果:", response.status_code, response.text)  # デバッグ用に送信結果を表示

@app.route("/webhook", methods=["GET"])
def verify_webhook():
    """Facebook Webhook の認証処理"""
    VERIFY_TOKEN = "1403ad4e4d93d83d317b3a6fbe5d14f1"  # ここに Webhook の検証トークンを設定
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    
    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("✅ Webhook Verified!")  # Webhook 認証成功
        return challenge, 200
    else:
        return "Verification Failed", 403  # 認証失敗

@app.route("/webhook", methods=["POST"])
def webhook():
    """Facebook Messenger からのメッセージ受信処理"""
    data = request.get_json()

    # 🔹 メッセージが送られた場合の処理
    messaging_event = data.get("entry", [{}])[0].get("messaging", [{}])[0]
    sender_id = messaging_event.get("sender", {}).get("id")  # 送信者のID
    message_text = messaging_event.get("message", {}).get("text", "")

    if sender_id and message_text:
        print(f"📩 受信: {sender_id} から「{message_text}」")
        send_message(sender_id, f"あなたのメッセージ: 「{message_text}」 を受け取りました！")  # 自動返信

    return "EVENT_RECEIVED", 200  # Facebook に正しく処理したことを通知

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
