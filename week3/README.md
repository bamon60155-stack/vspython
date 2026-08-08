# 多工具Agent：文档问答 + 数学计算 + 时间查询

基于LangChain构建的自主决策Agent，能根据用户问题自动判断该调用哪个工具（或不调用工具直接回答），整合了第二周实现的RAG检索能力。

## 功能介绍

- Agent能自主判断用户意图，在多个工具之间自主选择：
  - 查询当前日期时间
  - 数学表达式计算
  - 检索文档资料库（基于第二周的RAG实现）并生成有依据的回答
- 无需工具时，直接进行正常对话，不会误调用工具
- 向量库在程序启动时只构建一次，避免重复处理文档带来的性能问题和运行时错误

## 技术栈

- Python 3.13
- LangChain / LangChain-OpenAI（Agent与工具调用框架）
- LangGraph（Agent底层执行引擎）
- DeepSeek API（deepseek-v4-flash 模型）
- ChromaDB + sentence-transformers（向量检索，复用第二周的实现）

## 项目结构
├── agent_main.py # 主程序入口，初始化Agent并处理用户提问
├── tools.py # 所有工具定义：get_current_time、calculate、search_document
├── vector_store.py # 负责创建向量库（来自第二周）
├── document_loader.py # 负责文档切分（来自第二周）
├── paper.txt # 测试用文档
└── README.md

## 如何运行

1. 激活虚拟环境，安装依赖

```bash
pip install langchain langchain-openai langgraph chromadb sentence-transformers
```

2. 设置环境变量 `DEEPSEEK_API_KEY`

3. 运行

```bash
python agent_main.py
```

## 核心原理

### Function Calling 基础
在接触LangChain之前，先手写实现了最基础的Function Calling流程，理解了核心分工：**大模型只负责判断"要不要调用工具、调用哪个、参数是什么"，真正执行工具的是本地代码**，模型基于工具返回的真实结果生成最终回答。

### LangChain封装
用 `@tool` 装饰器定义工具（函数的文档字符串自动成为工具描述，供模型判断使用场景），`create_agent` 封装了"判断→执行→回传结果→生成回答"的完整循环，相比手写版本大幅简化了代码量。

### LangGraph条件分支（额外练习）
除了标准Agent，还实践了用LangGraph手动搭建带条件边（Conditional Edge）的流程图，实现"先分类问题类型，再路由到不同处理节点"的精细控制逻辑，理解了Agent（模型自主决策）和LangGraph（开发者精确控制流程）两种模式的适用场景差异。

## 项目过程中的关键问题与解决

**问题：`search_document` 工具每次被调用都报 `KeyError: 'ephemeral'`**

原因：最初把"读取文档、切分、建向量库"这几行代码写在了 `search_document` 函数内部，导致每次工具被调用（包括在LangGraph的多线程执行环境下）都会重新创建一次Chroma客户端，触发了Chroma在多线程场景下的已知兼容性问题，同时也造成了严重的性能浪费（每次提问都要重新处理一遍整个文档）。

解决：将向量库构建逻辑移到 `tools.py` 模块顶层，让它只在模块被导入时执行一次，`search_document` 函数内部只负责查询，复用已经建好的 `collection`。这也印证了一个通用原则：**"一次性的准备工作"和"每次调用都执行的逻辑"必须分离**，混在一起既低效，也容易引发难以排查的运行时错误。

## 后续计划

- 了解并尝试MCP协议的实际接入
- 探索多Agent协作（Multi-Agent）
- 结合卫星通信/RFFI背景做一个差异化项目