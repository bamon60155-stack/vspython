from langchain_core.tools import tool
from datetime import datetime
from vector_store import vector_store
from document_loader import split_by_paragraph

with open("week2/paper.txt", "r", encoding="utf-8") as f:
       sample_text = f.read()

chunks = split_by_paragraph(sample_text)
collection = vector_store(chunks)

@tool
def get_current_time() -> str:
    """获取当前的日期和时间,当用户询问现在几点、今天日期等问题时使用"""
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

@tool
def calculate(expression: str) -> str:
    """计算一个数学表达式的结果,比如输入3+5*2,当用户需要做数学计算式使用"""
    try:
        results = eval(expression)
        return str(results)
    except Exception as e:
        return f"计算出错：{e}"

@tool
def search_document(query: str) -> str:
    """搜索文档资料库， 当用户询问关于RAG、chunking、Embedding等相关技术文档内容时使用,输入用户的问题,返回相关的文档片段"""
    results = collection.query(query_texts=[query], n_results=4)
    retrieved_chunks = results["documents"][0]
    return "\n\n".join(retrieved_chunks)