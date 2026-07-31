from test_culting import split_text
import chromadb
from chromadb.utils import embedding_functions
from split_paragraph import split_by_paragraph
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
    name="my_paper_v2",
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

print(f"已存入{len(chunks)}块文本")

query = "RAG和微调比有什么优势?"

results = collection.query(
    query_texts=[query],
    n_results=2  # 返回最相似的2条
)

print(f"问题：{query}\n")
for doc, dist in zip(results["documents"][0], results["distances"][0]):
    print(f"[相似度距离：{dist:.3f}]")
    print(doc[:100] + "...")
    print("---")

print(f"总共切成了{len(chunks)}块")
for i, chunk in enumerate(chunks):
    print(f"---第{i+1}块---")
    print(chunk[:60] + "...")