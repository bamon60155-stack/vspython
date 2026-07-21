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
import os
from openai import OpenAI

client = OpenAI(
    api_key = os.environ.get("DEEPSEEK_API_KEY"),
    base_url= "https://api.deepseek.com"
)

response = client.chat.completions.create(
    model="deepseek-v4-pro",
    messages=[
        {"role": "system","content":"You are a helpful assistant"},
        {"role":"user", "content":"Hello"},
    ],
    stream=False,
    reasoning_effort="high",
    extra_body={"thinking": {"type": "enabled"}}
)

print(response.choices[0].message.content)