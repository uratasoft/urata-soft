def chatWithGPT(user_message):
    # ChatGPTへのリクエスト処理を関数化
    response = requests.post(...)
    return response.json()["choices"][0]["message"]["content"]