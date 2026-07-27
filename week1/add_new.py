import json
data = {"name": "思思", "age": 24, "skill": ["Python", "信号处理"]}

#写入json文件
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

#读取json文件
with open("data.json", "r", encoding="utf-8") as f:
    loaded_data = json.load(f)
    print(loaded_data)

#自己尝试
info = {"name": "糯米", "age": 3, "sex": "female", "skill": "可爱"}
with open("info.json", "w", encoding="utf-8") as f:
    json.dump(info, f, ensure_ascii=False, indent=2)

with open("info.json", "r", encoding="utf-8") as f:
    message = json.load(f)
    print(message)