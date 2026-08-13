from langchain_text_splitters import RecursiveCharacterTextSplitter
from clean_low_quality_chunk import is_low_quality_chunk
from vector_store import vector_store

splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100,
    separators=["\n\n", "\n", ". ", " ", ""]
)

all_chunks = []

paper_files = [
    "week4/starlink_paper.txt",
    "week4/fisher_info_paper.txt",
    "week4/pa_feature_paper.txt"
]

for file_path in paper_files:
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    chunks = splitter.split_text(text)
    good_chunks = [c for c in chunks if not is_low_quality_chunk(c)]
    all_chunks.extend(good_chunks)
    print(f"{file_path}: 切分{len(chunks)}块，过滤后{len(good_chunks)}块")

print(f"\n三篇论文总共有效chunk数:{len(all_chunks )}")

collection = vector_store(all_chunks, collection_name = "rffi_papers")

test_question = [
    "PA的memory polynomial模型是怎么定义的",
    "什么是IQ identifiability factor beta，它的作用是什么",
    "BPSK调制信号为什么无法识别IQ imbalance参数",
    "Starlink downlink信号的帧结构包含哪些部分",
    "如何估计PA模型的多项式阶数和记忆深度"
]

for q in test_question:
    print(f"\n问题:{q}")
    results = collection.query(query_texts=[q], n_results=4)
    for i, (doc, dist) in enumerate(zip(results["documents"][0], results["distances"][0])):
        print(f"  [{i+1}]距离{dist:.3f}: {doc[:80]}...")