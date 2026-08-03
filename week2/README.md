# RAG文档问答机器人

基于DeepSeek API + Chroma向量数据库实现的检索增强生成（RAG）系统，能够针对指定文档回答用户问题，并在资料不足时明确告知"无法回答"，而非编造答案。

## 功能介绍

- 将长文档按段落切分成语义完整的小块
- 使用Embedding模型将文本块转换为向量，存入Chroma向量数据库
- 用户提问时，自动检索最相关的文本块作为参考资料
- 基于检索到的资料生成回答，资料不足时不会编造答案
- 打印每次检索到的具体内容，便于调试和验证检索效果

## 技术栈

- Python 3.13
- DeepSeek API（deepseek-v4-flash 模型）
- ChromaDB（向量数据库）
- sentence-transformers（`paraphrase-multilingual-MiniLM-L12-v2`，中英文Embedding模型）

## 项目结构
├── main.py # 主程序入口，负责整体问答流程
├── document_loader.py # 负责文档切分（提供按段落切分、按固定长度切分两种策略）
├── vector_store.py # 负责创建向量库、存入文本
├── build_a_prompt.py # 负责组装RAG的Prompt
├── chat_client.py # 负责调用DeepSeek API、处理异常
├── paper.txt # 测试用文档
└── README.md
## 如何运行

1. 进入项目文件夹，创建并激活虚拟环境

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

2. 安装依赖

```bash
pip install openai chromadb sentence-transformers
```

3. 设置环境变量 `DEEPSEEK_API_KEY`（你自己的DeepSeek API Key）

4. 运行程序

```bash
python main.py
```

5. 在终端输入问题，输入 `exit` 退出

## 核心流程
文档 → 按段落切分 → 转换为向量 → 存入Chroma
↓
用户提问 → 转换为向量 → 检索最相关的几段 →
组装Prompt（资料+问题） → 发送给DeepSeek → 生成回答
## 项目过程中的关键发现

- **切分方式直接影响检索质量**：对比测试发现，固定长度切分（500字符一块）会把不同主题的内容硬拼在一起，导致检索排序不准确；改为按段落切分后，同一个查询的相似度距离从 0.6+ 降到 0.34，检索结果也更精准地命中了目标段落。
- **`n_results` 参数需要权衡**：设置过小（如2）会漏掉排名靠后但确实相关的内容，导致模型误判"无法回答"；调大到4后成功召回了完整的相关内容，但也需要注意检索数量过多会引入不相关的噪声。
- **Prompt设计对减少幻觉很关键**：明确要求模型"如果参考资料中没有相关信息，请说无法回答，不要编造"，能有效防止模型在资料不足时瞎编答案。

## 后续计划

- 接入真实PDF文档（当前仅支持纯文本，PDF提取和清洗尚未处理）
- 优化切分策略（探索递归切分、语义切分等更智能的方式）
- 接入Agent，让系统能自主判断"是否需要检索文档"
- 了解并尝试MCP协议