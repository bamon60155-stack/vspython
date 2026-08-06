from langchain_core.tools import tool
from datetime import datetime

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
