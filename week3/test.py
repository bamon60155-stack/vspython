from langchain_openai import ChatOpenAI
import os
from langchain_calling_demo import get_current_time,calculate

llm = ChatOpenAI(
    model = "deepseek-v4-flash",
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url = "https://api.deepseek.com"
)

from langchain.agents import create_agent

tools = [get_current_time, calculate]
agent = create_agent(llm, tools)

response = agent.invoke({"messages": [{"role":"user", "content": "你好，你是谁"}]})

# 打印最后一条消息（也就是agent最终的回答）
print(response["messages"][-1].content)