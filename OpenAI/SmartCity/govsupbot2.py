# スマートシティ市役所のAI総合案内用プログラム
# Web開発用フレームワークFlaskを使用
from flask import Flask, request
import openai
import json
import os

# Web開発するためのフレームワークFlaskを使用
# Flaskアプリインスタンス生成
app = Flask(__name__)

# 環境変数からAPI_KEYを取得する
plus_key = os.environ["OPENAI_PLUS_KEY"]
client = openai.Client(api_key=plus_key)

@app.route("/chat", methods=["POST"])
def chat():
    try:
        # JSONデータをSHIFT_JISで強制デコード
        data = request.data.decode("shift_jis", errors="ignore")  
        json_data = json.loads(data)  # JSON デコード

        if not json_data or "message" not in json_data:
            return app.response_class(
                response=json.dumps({"error": "Invalid JSON: 'message' field is required"}, ensure_ascii=False),
                status=400,
                mimetype="application/json"
            )
        
        user_input = json_data["message"]
        print(user_input)
        
        messages=[
                {"role": "system", "content": 
                 "あなたは流山市役所のAI総合案内係です。"
                 "流山市役所職員として各申請手続きの方法などを案内してやってください。"
                 "また、可能な限り一般的な質問にも答えるようにしてください。"
                 "来訪者の質問が不明確な場合は、どのような情報が必要か聞いてやってください。"},
                {"role": "user", "content": user_input}
            ]
        
        responses = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=300,
            temperature=0.7
        )
        
        reply = responses.choices[0].message.content.strip()

        # 🔥 JSON レスポンスの Unicode エスケープを防ぐ
        return app.response_class(
            response=json.dumps({"response": reply}, ensure_ascii=False), 
            status=200, 
            mimetype="application/json"
        )

    except json.JSONDecodeError:
        return app.response_class(
            response=json.dumps({"error": "Invalid JSON format"}, ensure_ascii=False),
            status=400,
            mimetype="application/json"
        )
    except UnicodeDecodeError:
        return app.response_class(
            response=json.dumps({"error": "Encoding error: Ensure Shift_JIS encoding"}, ensure_ascii=False),
            status=400,
            mimetype="application/json"
        )
    except Exception as e:
        return app.response_class(
            response=json.dumps({"error": str(e)}, ensure_ascii=False),
            status=500,
            mimetype="application/json"
        )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

