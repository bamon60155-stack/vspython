import chromadb
from chromadb.utils import embedding_functions
from document_loader import split_by_paragraph
from build_a_prompt import build_prompt
from chat_client import create_client, get_ai_reply
from vector_store import vector_store

def main():
    with open("week2/paper.txt", "r", encoding="utf-8") as f:
     sample_text = f.read()

    chunks = split_by_paragraph(sample_text)

    collection = vector_store(chunks)
    client = create_client()
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

if __name__ == "__main__":
   main()