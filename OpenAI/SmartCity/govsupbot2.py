from flask import Flask, request, jsonify
import openai
import json

app = Flask(__name__)

client = openai.Client(api_key="YOUR_OPENAI_API_KEY")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        # JSONデータを UTF-8 で強制デコード
        data = request.data.decode("utf-8")  
        json_data = json.loads(data)  # JSON デコード

        if not json_data or "message" not in json_data:
            return jsonify({"error": "Invalid JSON: 'message' field is required"}), 400
        
        user_input = json_data["message"]
        print(f"Received JSON request: {request.json}")  # リクエスト全体を確認
        print(f"Received user input: {user_input}")  # ユーザー入力内容を確認

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                #{"role": "system", "content": "あなたは流山市役所のFAQアシスタントです。"},
                {"role": "system", "content": "あなたは流山市役所のAI総合案内係です。市役所職員として親切に回答してください。"},
                {"role": "user", "content": user_input}
            ],
            max_tokens=200
        )
        
        reply = response.choices[0].message.content.strip()

        # 🔥 JSON レスポンスの Unicode エスケープを防ぐ
        return app.response_class(
            response=json.dumps({"response": reply}, ensure_ascii=False), 
            status=200, 
            mimetype="application/json"
        )
        # APIレスポンスを表示
        print(f"API Response: {response}")  # レスポンス全体を確認

    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON format"}), 400
    except UnicodeDecodeError:
        return jsonify({"error": "Encoding error: Ensure UTF-8 encoding"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
