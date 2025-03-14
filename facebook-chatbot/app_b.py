import os
import requests
from flask import Flask, request

app = Flask(__name__)

# ✅ Webhook の検証トークン（Facebook の設定と一致させる）
VERIFY_TOKEN = "1403ad4e4d93d83d317b3a6fbe5d14f1"

@app.route("/", methods=["GET"])
def home():
    """Flask の動作確認用エンドポイント"""
    return "Flask is running!", 200

@app.route("/webhook", methods=["GET"])
def verify():
    """Facebook Webhook の検証用エンドポイント"""
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    print(f"🔍 GETリクエスト受信: mode={mode}, token={token}, challenge={challenge}")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("✅ Webhook Verified!")
        return challenge, 200
    else:
        print("❌ Verification Failed!")
        return "Verification Failed", 403

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
