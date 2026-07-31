def split_by_paragraph(text):
    """
    按段落切分文本，以连续的换行符作为分隔标志
    """
    paragraphs = text.split("\n\n")  # 按“两个换行符”切开
    # 顺手清理一下，去掉可能存在的空段落、以及每段前后多余的空格
    paragraphs = [p.strip() for p in paragraphs if p.strip() !=""]
    return paragraphs
