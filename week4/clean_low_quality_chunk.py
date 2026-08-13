import re

def is_low_quality_chunk(text, min_length=50):
    """
    判断一个文本块是否是低质量/乱码块
    返回True表示应该丢弃
    """

    # 太短的快，信息量太少，价值不大
    if len(text) < min_length:
        return True

    # 包含明显的PDF提取乱码标记
    if "(cid:" in text:
        return True

    # 计算字母数字字符的占比， 占比太低说明可能是乱码/公式碎片
    alnum_count = sum(c.isalnum() for c in text)
    ratio = alnum_count / len(text)
    if ratio < 0.5:
        return True

    # 检查孤立数字行的密度（公式下标的典型特征）
    lines = text.split("\n")
    isolated_number_lines = sum(1 for line in lines if line.strip().replace(" ","").isdigit())
    if len(lines) > 0 and isolated_number_lines / len(lines) > 0.3:
        return True

    return False