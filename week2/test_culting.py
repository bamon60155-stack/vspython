def split_text(text, chunk_size=500, overlap=50):
    """
    把长文本按固定字数切分成小块
    text: 原始长文本
    chunk_size: 每一块的字数
    overlap: 相邻两块之间重叠的字数（防止切分点正好切断一个重要的句子/意思）
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += (chunk_size - overlap) # 下一块的起点，往回退一点，形成重叠
    return chunks
