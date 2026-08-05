from typing import TypedDict

class AgentState(TypedDict):
    question: str          # 用户的原始问题
    question_type: str      # 判断出来的问题类型
    answer: str            # 最终答案


