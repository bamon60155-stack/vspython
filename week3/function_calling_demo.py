tools = [
    {
        "type":"function",
        "function":{
            "name":"get_current_time",
            "description":"获取当前的日期和时间，当用户询问现在几点、今天日期等问题时使用",
            "paramaters":{
                "type":"object",
                "properties":{},
                "required":[]
            }
        }
    }
]

import os
import json
from openai import OpenAI
from get_current_time import get_current_time

client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

messages = [
    {"role":"user", "content":"现在几点了？"}
]

response = client.chat.completions.create(
    model="deepseek-v4-flash",
    messages=messages,
    tools=tools   # 把工具描述传给模型
)

print(response.choices[0].message)

message = response.choices[0].message

if message.tool_calls:
    # 模型判断需要调用工具
    tool_call = message.tool_calls[0]
    function_name = tool_call.function.name
    print(f"模型觉得调用工具:{function_name}")

    # 真正执行这个工具（这一步是你的代码在做，不是模型在做）
    if function_name == "get_current_time":
        result = get_current_time()

    # 把工具执行的结果，加进对话历史，再发回给模型
    messages.append(message)  # 先把模型要调用工具这个请求记录下来
    messages.append({
        "role":"tool",
        "tool_call_id": tool_call.id,
        "content":result
    })

    # 让模型基于这个真实结果，生成最终的自然语言回答
    second_response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=messages
    )
    print(second_response.choices[0].message.content)

else:
    # 模型判断不需要调用工具，直接回答
    print(message.content)