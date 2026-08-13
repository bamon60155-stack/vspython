from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from tools import get_current_time, search_document, calculate_crb
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
import os

# 初始化，只执行一次
app = FastAPI()
# 新增：告诉FastAPI，static文件夹里的东西可以被访问
app.mount("/static", StaticFiles(directory="static"), name="static")

llm = ChatOpenAI(
    model="deepseek-v4-flash",
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

tools = [get_current_time, search_document, calculate_crb]
agent = create_agent(llm, tools)

# 定义请求数据的格式
class ChatRequest(BaseModel):
    question: str

#  访问网站首页时，返回这个HTML页面
@app.get("/")
def home():
    return FileResponse("static/index.html")


# 定义接口
@app.post("/chat")
def chat(request: ChatRequest):
    response = agent.invoke({"messages":[{"role": "user", "content": request.question}]})
    answer = response["messages"][-1].content
    return {"answer":answer}