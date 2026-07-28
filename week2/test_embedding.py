from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

sentences = [
    "我喜欢狗",
    "我很爱我的宠物",
    "今天天气怎么样",
    "卫星通信技术"
]

embeddings = model.encode(sentences)
similarity_matrix = cosine_similarity(embeddings)

print(embeddings.shape)
print(embeddings[0][:10])
print(similarity_matrix)