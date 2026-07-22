# with open("note.txt", "r", encoding="utf-8") as f:
#     content = f.readlines()

# #readlines每次读取一行，做成列表

# data = {"main":"今日学习内容", "note": content}

# import json
# with open("new.json", "w", encoding="utf-8") as f:
#     json.dump(data, f, ensure_ascii=False, indent=2)

# with open("new.json", "r", encoding="utf-8") as f:
#     message = json.load(f)
#     print(message)
# 
# import requests

# response = requests.get("https://api.github.com")
# print(response.status_code)
# print(response.text)

# data = response.json()
# print(data["starred_url"])

# import os
# import requests

# api_key = os.environ.get("DEEPSEEK_API_KEY")
# url = "https://api.deepseek.com/chat/completions"
# headers = {
#     "Content-Type":"application/json",
#     "Authorization":f"Bearer {api_key}"
# }
# data = {
#     "model":"deepseek-v4-flash",
#     "messages":[
#         {"role": "user","content":"我喜欢你"}
#     ]
# }

# response = requests.post(url, headers=headers, json=data)
# result = response.json()
# print(result["choices"][0]["message"]["content"])

import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")

messages = [ {"role": "system", "content": "You are a helpful assistant"}]

while True:
    user_input = input("user:")
    if user_input == "exit":
        print("再见！")
        break
    messages.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(
       model = "deepseek-v4-flash",
       messages = messages,
       stream = False,
    #    reasoning_effort="high",
    #    extra_body={"thinking": {"type": "enabled"}}
    )

    print("AI:" + response.choices[0].message.content)
    ai_reply = response.choices[0].message.content
    messages.append({"role":"assistant","content":ai_reply})

# while True:
#     number = input("请输入数字：")
#     if number == "stop":
#         break
#     number = int(number)
#     print(f"该数字翻倍是{number*2}")