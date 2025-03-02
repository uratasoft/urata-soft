from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)
client = OpenAI(api_key="OPENAI_PLUS_KEY")

@app.route("/chat", methods=["POST"])
def chat():
    # リクエストからメッセージを取得
    try:
        user_input = request.json.get("message", "")
        print(f"Received JSON request: {request.json}")  # リクエスト全体を確認
        print(f"Received user input: {user_input}")  # ユーザー入力内容を確認
    except Exception as e:
        print(f"Error parsing JSON: {e}")  # JSON の解析エラーを確認
        return jsonify({"error": "Invalid JSON format"}), 400

    # メッセージが空でないことを確認
    if not user_input:
        print("No user input provided.")  # 空の入力が送信された場合
        return jsonify({"error": "No message provided"}), 400

    # OpenAI API用のメッセージ形式に変換
    messages = [
        {"role": "system", "content": "あなたは流山市役所のAI総合案内係です。市役所職員として親切に回答してください。"},
        {"role": "user", "content": user_input}
    ]
    
    # messages の確認
    print(f"Formatted messages for OpenAI: {messages}")  # messages が正しく構成されているか確認

    # OpenAI APIを呼び出す
    try:
        response = client.chat.completions.create(
            model="gpt-4",  # モデル名
            messages=messages,
            max_tokens=300,
            temperature=0
        )
        
        # APIレスポンスを表示
        print(f"API Response: {response}")  # レスポンス全体を確認

        # 結果を返す
        return jsonify({
            "status": "success",
            "response": response.choices[0].message.content.strip()
        })
    except Exception as e:
        # エラーが発生した場合、エラーメッセージを表示
        print(f"Error occurred: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
