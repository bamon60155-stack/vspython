from tools import get_current_time, calculate, search_document
from vector_store import vector_store
from document_loader import split_by_paragraph
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
import os

llm = ChatOpenAI(
    model="deepseek-v4-flash",
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

tools = [get_current_time, calculate, search_document]
agent = create_agent(llm, tools)

response1 = agent.invoke({"messages":[{"role": "user", "content": "RAG和微调相比有什么优势？"}]})
print(response1["messages"][-1].content)

# 应该会调用calculate，而不是search_document
response2 = agent.invoke({"messages": [{"role": "user", "content": "帮我算一下100除以4"}]})
print(response2["messages"][-1].content)

# 应该都不调用
response3 = agent.invoke({"messages": [{"role": "user", "content": "你好"}]})
print(response3["messages"][-1].content)