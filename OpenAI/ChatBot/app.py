import os
from openai import OpenAI
from search import answer_question
client = OpenAI()


# 最初にメッセージを表示する
print("質問を入力してください")

conversation_history = [
{"role": "system", "content":  "あなたは世界的に有名な詩人です。詩的な比喩表現を使って回答してください"}
]

while True:
    # ユーザーの入力した文字を変数「user_input」に格納
    user_input = input()

    # ユーザーの入力した文字が「exit」の場合はループを抜ける
    if user_input == "exit":
        break
    
    conversation_history.append({"role": "user", "content": user_input})
    answer = answer_question(user_input, conversation_history)

    print("ChatGPT:", answer)
    conversation_history.append({"role": "assistant", "content":answer})
