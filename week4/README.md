# Satellite RFFI RAG Agent

## 项目简介

本项目是一个面向**卫星通信与射频指纹识别（Radio Frequency Fingerprint Identification, RFFI）**领域的智能问答系统。

项目以卫星通信、Starlink、Iridium、功放非线性、IQ 不平衡、Fisher 信息量以及 Cramér-Rao 下界（CRB）等相关论文作为知识来源，结合 **RAG（Retrieval-Augmented Generation，检索增强生成）**、**Agent 工具调用**、**FastAPI Web 服务**和 **Docker 容器化部署**，实现专业文献问答、参数计算和工具调用等功能。

系统不仅可以直接回答普通问题，还能够根据用户意图自动决定是否调用文档检索工具、CRB 计算工具或时间查询工具。

---

## 主要功能

### 1. 专业文献 RAG 问答

系统能够从本地卫星通信与 RFFI 文献知识库中检索相关内容，并基于检索结果生成回答。

目前知识库主要覆盖：

- Starlink Ku 波段下行信号结构
- 卫星射频指纹识别
- Iridium / Starlink 发射机硬件特征
- 功放（PA）非线性
- IQ 不平衡
- Fisher Information Matrix（FIM）
- Cramér-Rao Bound（CRB）
- 射频指纹参数可辨识性
- 深度学习 RFFI 方法

例如：

```text
论文中关于功放非线性或射频指纹特征的内容是什么？
```

系统会调用文档检索工具，在知识库中查找相关论文片段，并结合检索结果生成回答。

---

### 2. Agent 智能工具调用

项目使用 LangChain Agent，使大模型能够根据用户问题自动判断是否需要调用外部工具。

目前包含以下工具：

#### 文档检索工具

```text
search_document
```

用于从向量知识库中检索与用户问题相关的论文内容。

---

#### CRB 计算工具

```text
calculate_crb
```

根据调制方式、已知符号数和信噪比计算射频指纹参数的 Cramér-Rao 下界。

支持的调制方式包括：

- BPSK
- QPSK
- 8PSK
- 16QAM
- 64QAM

主要计算：

- IQ 不平衡参数 ε 的 CRB
- PA 非线性参数 Re(α₃) 的 CRB
- IQ 参数可辨识性

例如：

```text
请计算 QPSK、N=1000、SNR=20dB 时的 CRB。
```

系统会自动调用 CRB 计算工具并返回结果。

---

#### 时间查询工具

```text
get_current_time
```

用于获取当前北京时间。

---

### 3. 异常参数校验

系统对工具输入进行基本合法性检查。

例如：

```text
帮我计算 QPSK、N=-100、SNR=20dB 的 CRB。
```

系统不会自动修改用户参数，而是返回：

```text
N 必须为正整数
```

避免大模型在未经用户确认的情况下修改计算条件。

---

### 4. 知识库边界控制

当用户询问的专业问题不在知识库范围内时，系统能够明确说明未检索到相关内容，而不是直接将不存在的信息归因于知识库。

例如：

```text
这些论文有没有研究 GPS L1 C/A 信号的欺骗检测算法？
```

系统会说明当前知识库没有针对 GPS L1 C/A 欺骗检测的专门研究，并区分：

```text
知识库已有结论
```

和

```text
模型扩展分析
```

降低 RAG 系统产生知识库幻觉的风险。

---

## 系统架构

整体流程如下：

```text
用户输入
   ↓
FastAPI Web 接口
   ↓
LangChain Agent
   ↓
意图判断
   │
   ├── 普通问题
   │      ↓
   │     LLM
   │
   ├── 文献问题
   │      ↓
   │ search_document
   │      ↓
   │ Vector Store
   │      ↓
   │ 相关论文片段
   │
   ├── CRB 计算
   │      ↓
   │ calculate_crb
   │
   └── 时间查询
          ↓
     get_current_time
          ↓
        LLM
          ↓
      最终回答
          ↓
       Web 页面
```

---

## 技术栈

### 大模型与 Agent

- DeepSeek API
- LangChain
- LangChain OpenAI Integration
- LangGraph / Agent

### RAG

- ChromaDB
- Embedding
- 文档切分
- 向量相似度检索

### 后端

- Python
- FastAPI
- Uvicorn
- Pydantic

### 前端

- HTML
- CSS
- JavaScript

### 工程化

- Python Virtual Environment
- requirements.txt
- Docker
- WSL 2
- Docker Desktop

---

## 项目目录

项目核心目录结构如下：

```text
week4/
│
├── static/
│   └── index.html
│
├── api.py
├── main.py
├── tools.py
├── vector_store.py
├── document_loader.py
│
├── clean_pdf_text.py
├── test_pdf.py
│
├── starlink_paper.txt
├── fisher_info_paper.txt
├── pa_feature_paper.txt
│
├── *.pdf
│
├── requirements.txt
├── Dockerfile
└── .dockerignore
```

主要文件说明：

### `api.py`

FastAPI 服务入口。

主要负责：

- 创建 FastAPI 应用
- 初始化 LLM
- 创建 Agent
- 注册工具
- 提供 `/chat` API
- 提供 Web 首页

---

### `tools.py`

定义 Agent 可以调用的工具，包括：

```text
get_current_time
search_document
calculate_crb
```

---

### `vector_store.py`

负责向量数据库相关功能，包括：

- 文档 Embedding
- ChromaDB 存储
- 相似度检索

---

### `document_loader.py`

负责：

- 文档加载
- 文本预处理
- 文档切分

---

### `static/index.html`

简单 Web 聊天页面，通过 HTTP 请求调用：

```text
POST /chat
```

并显示大模型回答。

---

## FastAPI 接口

### Web 首页

```http
GET /
```

返回：

```text
static/index.html
```

---

### Chat API

```http
POST /chat
```

请求示例：

```json
{
  "question": "请计算 QPSK、N=1000、SNR=20dB 时的 CRB。"
}
```

返回示例：

```json
{
  "answer": "..."
}
```

---

## 本地运行

首先安装项目依赖：

```bash
pip install -r requirements.txt
```

配置 DeepSeek API Key。

Windows PowerShell：

```powershell
$env:DEEPSEEK_API_KEY="your_api_key"
```

启动 FastAPI：

```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```

浏览器访问：

```text
http://localhost:8000
```

---

## Docker 部署

项目支持通过 Docker 进行容器化运行。

### Dockerfile

```dockerfile
FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 构建镜像

```bash
docker build -t rag-agent .
```

### 启动容器

Windows PowerShell：

```powershell
docker run -p 8000:8000 -e DEEPSEEK_API_KEY=$env:DEEPSEEK_API_KEY rag-agent
```

其中：

```text
-p 8000:8000
```

表示：

```text
Windows 8000端口
        ↓
Docker Container 8000端口
        ↓
FastAPI
```

浏览器访问：

```text
http://localhost:8000
```

即可使用 Docker 中运行的 Agent。

---

## 项目测试

项目完成后进行了多组功能与边界测试。

| 测试内容 | 预期行为 | 测试结果 |
|---|---|---|
| “你好，你能做什么？” | 普通对话，不进行无关工具调用 | 通过 |
| “论文中关于功放非线性的内容是什么？” | 调用文档检索 | 通过 |
| “现在几点？” | 调用时间工具 | 通过 |
| “QPSK、N=1000、SNR=20dB 的 CRB” | 调用 CRB 工具 | 通过 |
| “N=-100 的 CRB” | 拒绝非法参数 | 通过 |
| “爱因斯坦哪年出生？” | 普通知识回答，不强制使用知识库 | 通过 |
| “论文是否研究 GPS L1 C/A 欺骗检测？” | 检索知识库并明确说明不存在 | 通过 |

---

## 测试过程中发现的问题与优化

### 1. Python 环境不一致

开发电脑中同时存在多个 Python 环境，包括 Python 3.8 和 Python 3.13。

最初生成 `requirements.txt` 时使用了错误的 Python 环境，导致依赖中缺少：

```text
fastapi
uvicorn
langchain
langchain-openai
```

并包含与项目无关的依赖。

后续统一使用项目虚拟环境重新生成依赖文件。

---

### 2. Docker Python 版本不一致

项目虚拟环境使用 Python 3.13，而初始 Dockerfile 使用：

```dockerfile
FROM python:3.11-slim
```

导致：

```text
numpy==2.5.1
```

无法安装。

最终将 Docker 环境修改为：

```dockerfile
FROM python:3.13-slim
```

保证开发环境与部署环境一致。

---

### 3. 时间工具时区问题

初始版本返回 UTC 时间。

优化后使用：

```text
Asia/Shanghai
```

返回北京时间。

---

### 4. CRB 非法输入问题

初始 Agent 在用户输入：

```text
N=-100
```

时会自行修改为：

```text
N=100
```

并继续计算。

后续在工具层增加严格参数检查：

```text
N <= 0
```

时直接返回错误，不允许自动修改用户输入。

---

### 5. RAG 知识边界

对知识库之外的问题进行测试后，系统能够明确说明未检索到相关论文，而不是将模型自身知识错误归因于知识库。

---

## 项目亮点

### RAG 与 Agent 结合

项目并非单纯的文档问答，而是将：

```text
RAG
+
Agent
+
Tool Calling
```

结合，使模型能够自主选择不同工具处理不同任务。

---

### 与实际科研方向结合

知识库内容来自卫星通信与射频指纹识别相关研究，项目不是通用 Demo，而是结合实际专业研究方向构建。

---

### 理论工具集成

将 CRB / Fisher Information 等理论计算封装为 Agent 工具，使系统能够同时完成：

```text
文献查询
+
理论计算
+
结果解释
```

---

### 工程化部署

项目最终通过：

```text
FastAPI
+
Web
+
Docker
```

完成从命令行程序到可访问 Web 服务的转换。

---

## 后续可优化方向

1. 增加论文来源引用和页码定位；
2. 优化文档 Chunk 切分策略；
3. 增加 Reranker 提升检索准确率；
4. 增加多轮对话 Memory；
5. 增加流式输出；
6. 增加模型调用日志与 Agent 工具调用日志；
7. 对 CRB 工具增加更严格的输入 Schema；
8. 增加 Docker Compose；
9. 部署到云服务器；
10. 增加用户上传 PDF 后自动构建知识库的功能。

---

## 项目总结

本项目完成了一个从本地专业文档出发的完整大模型应用流程：

```text
论文文档
   ↓
文本处理
   ↓
Embedding
   ↓
Vector Store
   ↓
RAG
   ↓
Agent
   ↓
Tool Calling
   ↓
FastAPI
   ↓
Web UI
   ↓
Docker
```

通过本项目，完成了从大模型 API 调用、RAG 文档检索、Agent 工具调用，到 Web 服务和 Docker 容器化部署的完整实践。

该项目同时结合卫星通信与射频指纹识别研究方向，使大模型应用开发与实际科研任务相结合。