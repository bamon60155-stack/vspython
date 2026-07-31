# from test_culting import split_text  # 这个不好用先不用了
import chromadb
from chromadb.utils import embedding_functions
from split_paragraph import split_by_paragraph
from build_a_prompt import build_prompt
from chat_client import create_client, get_ai_reply
# 第一种路径方法
# 第一步：读取文本，切分成小块
with open("week2/paper.txt", "r", encoding="utf-8") as f:
    sample_text = f.read()

# 第二种路径方法
# import os

# current_dir = os.path.dirname(os.path.abspath(__file__))
# file_path = os.path.join(current_dir, "paper.txt")
# with open(file_path, "r", encoding="utf-8") as f:
#     sample_text = f.read()

# chunks = split_text(sample_text, chunk_size=500, overlap=50)
chunks = split_by_paragraph(sample_text)

# 第二步：创建Chroma客户端和collection
chroma_client = chromadb.Client()
# collection = chroma_client.create_collection(name="my_paper")
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="paraphrase-multilingual-MiniLM-L12-v2"
)

collection = chroma_client.create_collection(
    name="test_demo",
    embedding_function=sentence_transformer_ef
)

# print(f"总共切成了{len(chunks)}块")
# for i, chunk in enumerate(chunks):
#     print(f"---第{i+1}块（长度{len(chunk)}字符）---")
#     print(chunk[:50] + "...") # 只打印每块的前50个字符，方便快速浏览

# 第三步：把切好的每一块，存进collection
# Chroma要求每一条数据都要有一个唯一的id，用列表推导式批量生成
ids = [f"chunk_{i}" for i in range(len(chunks))]

# chroma有内嵌的embedding模型，没有指定embedding的模型，chroma会使用自己内置的默认小模型
collection.add(
    documents=chunks,  # 文本内容列表
    ids=ids            # 对应的唯一编号列表
)

print(f"文档已切成{len(chunks)}块文本，并存入向量库")

# =====第三步：定义组装prompt的函数 =====
# 已经定义过了

# =====第四步：创建ds客户端 =====
client = create_client()

# =====第五步：主循环，实现完整RAG问答 =====
while True:
    question = input("\n你的问题(输入exit退出):")
    if question == "exit":
        print("再见！")
        break
    if question.strip() == "":
        print("请输入内容")
        continue

    # 检索最相关的2段
    results = collection.query(query_texts=[question], n_results=4)
    retrieved_chunks = results["documents"][0]

    # 加这两行调试
    print("\n[调试] 本次检索到的内容：")
    for chunk in retrieved_chunks:
         print(chunk[:50] + "...")

    # 组装prompt
    rag_prompt = build_prompt(question, retrieved_chunks)

    # 发给大模型
    message = [
        {"role":"system", "content":"你是一个基于给定资料回答问题的助手"},
        {"role":"user", "content": rag_prompt}
    ]

    answer = get_ai_reply(client, message)

    print(f"\nAI回答:{answer}")


