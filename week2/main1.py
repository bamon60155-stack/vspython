from test_culting import split_text

with open("week2/paper.txt", "r", encoding="utf-8") as f:
    sample_text = f.read()

chunks = split_text(sample_text, chunk_size=500, overlap=50)

print(f"总共切成了{len(chunks)}块")
for i, chunk in enumerate(chunks):
    print(f"---第{i+1}块（长度{len(chunk)}字符）---")
    print(chunk[:50] + "...") # 只打印每块的前50个字符，方便快速浏览