import os
from openai import OpenAI, AuthenticationError, APIConnectionError, RateLimitError

def create_client():
    """创建并且返回一个deepseek客户端"""
    client = OpenAI(
        api_key = os.environ.get("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com"
    )
    return client

def get_ai_reply(client, messages):
    """
    传入客户端和聊天记录,返回AI的回复文字
    如果出错,返回一个以“错误:”开头的提示字符串
    """
    try:
        response = client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=messages,
            stream = False
        )
        return response.choices[0].message.content

    except AuthenticationError:
        return "错误:身份验证失败, 请检查API Key"
    except APIConnectionError:
        return "错误:网络连接失败，请检查网络或代理设置"
    except RateLimitError:
        return "错误:请求太频繁,请稍后再试"
    except Exception as e:
        return f"错误:发生了未知问题{e}"
