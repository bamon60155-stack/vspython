def build_prompt(question, retrived_chunks):
    context = "\n\n".join(retrived_chunks)   #把检索到的几段，用空行拼接成一整段参考资料

    prompt = f"""请根据下面提供的参考资料，回答用户的问题。如果参考资料中没有相关信息，请明确说"根据现有资料无法回答"，不要编造答案。

参考资料：
{context}

用户问题：{question}

请给出准确、简洁的回答：
"""
    return prompt