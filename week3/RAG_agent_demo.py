from vector_store import vector_store
from document_loader import split_by_paragraph

with open("week2/paper.txt", "r", encoding="utf-8") as f:
    sample_text = f.read()

chunks = split_by_paragraph(sample_text)
collection = vector_store(chunks)

from langchain_core.tools import tool

@tool
def search_document(query: str) -> str:
    """搜索文档资料库， 当用户询问关于RAG、chunking、Embedding等相关技术文档内容时使用,输入用户的问题,返回相关的文档片段"""
    results = collection.query(query_texts=[query], n_results=4)
    retrieved_chunks = results["documents"][0]
    return "\n\n".join(retrieved_chunks)

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
import os
from langchain_calling_demo import get_current_time, calculate

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