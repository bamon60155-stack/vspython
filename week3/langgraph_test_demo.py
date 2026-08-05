from typing import TypedDict

class AgentState(TypedDict):
    question: str          # 用户的原始问题
    question_type: str      # 判断出来的问题类型
    answer: str            # 最终答案


import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# 节点1：判断问题类型
def classify_question(state: AgentState):
    question = state["question"]

    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=[
            {"role": "system", "content": "判断用户问题属于'math'、'time'还是'other'，只回答这三个词中的一个，不要多余内容"},
            {"role": "user", "content": question}
        ]
    )
    question_type = response.choices[0].message.content.strip()
    return {"question_type": question_type}


# 节点2：处理数学问题
def handle_math(state:AgentState):
    question = state["question"]
    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=[{"role": "user", "content": f"请计算：{question}"}]
    )
    return {"answer": response.choices[0].message.content}

# 节点3: 处理时间问题
def handle_time(state:AgentState):
    from datetime import datetime
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"answer": f"当前时间是；{now}"}


# 节点4：处理其他问题
def handle_other(state: AgentState):
    question = state["question"]
    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=[{"role": "user", "content": question}]
    )
    return {"answer": response.choices[0].message.content}

def route_question(state: AgentState):
    question_type = state["question_type"]
    if question_type == "math":
        return "math"
    elif question_type == "time":
        return "time"
    else:
        return "other"


from langgraph.graph import StateGraph, END

# 创建一个"流程图构建器"，告诉它这个流程图里传递的state长什么样
graph_builder = StateGraph(AgentState)

# 把每个节点加进图里，起个名字
graph_builder.add_node("classify", classify_question)
graph_builder.add_node("math", handle_math)
graph_builder.add_node("time", handle_time)
graph_builder.add_node("other", handle_other)

# 设置入口：流程从哪个节点开始
graph_builder.set_entry_point("classify")

# 添加条件边：做完classify之后，根据route_question的判断结果，走向不同节点
graph_builder.add_conditional_edges(
    "classify",     # 从哪个节点出发
    route_question,     # 用哪个函数来判断
   {
       "math": "math",
       "time": "time",
       "other": "other"
   } 
)

# 三个处理节点做完之后，流程就结束了
graph_builder.add_edge("math", END)
graph_builder.add_edge("time", END)
graph_builder.add_edge("other", END)

# 编译成一个可以运行的图
graph = graph_builder.compile()

results1 = graph.invoke({"question":"帮我算一下17乘以23","question_type": "", "answer": "" })
print(results1["answer"])

result2 = graph.invoke({"question": "现在几点了？", "question_type": "", "answer": ""})
print(result2["answer"])

result3 = graph.invoke({"question": "推荐一本科幻小说", "question_type": "", "answer": ""})
print(result3["answer"])