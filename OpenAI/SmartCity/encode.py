import requests
import json

url = "http://127.0.0.1:5000/chat"

headers = {"Content-Type": "application/json; charset=utf-8"}
data = {"message": "流山市のゴミ収集日は？"}

response = requests.post(url, headers=headers, data=json.dumps(data, ensure_ascii=False).encode("utf-8"))

def new_func(response):
    print(response.json())

new_func(response)