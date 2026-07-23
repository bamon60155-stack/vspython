# 命令行AI对话助手

一个基于DeepSeek API的命令行对话程序，支持连续多轮对话（能记住上下文）。

## 功能介绍

- 在终端中与AI进行连续对话
- 自动维护对话历史，AI能记住之前聊过的内容
- 包含异常处理：API Key错误、网络连接失败、请求超限等情况都有对应提示
- 输入 `exit` 可退出程序

## 技术栈

- Python 3.13
- OpenAI SDK（用于兼容DeepSeek的API调用格式）
- DeepSeek API（deepseek-v4-flash 模型）

## 项目结构
├── main.py # 主程序入口，负责整体对话流程
├── chat_client.py # 负责调用DeepSeek API、处理异常
└── README.md
## 如何运行

1. 克隆本项目到本地

```bash
git clone 你的仓库地址
```

2. 创建虚拟环境并激活

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

3. 安装依赖

```bash
pip install openai
```

4. 设置环境变量 `DEEPSEEK_API_KEY`（你自己的DeepSeek API Key）

5. 运行程序

```bash
python main.py
```

## 后续计划

- 加入RAG（检索增强生成）功能
- 加入Agent（多工具调用）能力