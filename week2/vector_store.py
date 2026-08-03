import chromadb
from chromadb.utils import embedding_functions

def vector_store(chunks):
    # 创建Chroma客户端和collection
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

    # 把切好的每一块，存进collection
    # Chroma要求每一条数据都要有一个唯一的id，用列表推导式批量生成
    ids = [f"chunk_{i}" for i in range(len(chunks))]

    # chroma有内嵌的embedding模型，没有指定embedding的模型，chroma会使用自己内置的默认小模型
    collection.add(
    documents=chunks,  # 文本内容列表
    ids=ids            # 对应的唯一编号列表
    )

    print(f"文档已切成{len(chunks)}块文本，并存入向量库")
    return collection