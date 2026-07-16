print ("你好思思")
print ("我很想你")
print ("施施我很想你呀")
# 打开txt文件
# 模式有三种，r，w（内容如果存在会被清空重写），a（追加append）
f = open("文件名.txt", "模式", encoding="utf-8")
f.close()
# 更推荐的另一种写法 自动帮我关闭文件
# 写txt文件
with open("test.txt", "w", encoding="utf-8") as f:
    f.write("i am so fucking tired")
# 读取txt文件
with open("test.txt", "r", encoding="utf-8") as f:
    content = f.read()
    # read()函数是吧整个文件内容读成一个字符串
    # readlines()是把每一行读成列表的一个元素
    print(content)
    


