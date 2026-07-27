print ("你好思思")
print ("我很想你")
print ("施施我很想你呀")
# 打开txt文件
# 模式有三种，r，w（内容如果存在会被清空重写），a（追加append）
#f = open("文件名.txt", "模式", encoding="utf-8")
#f.close()
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

#自己尝试
with open("note.txt", "w", encoding="utf-8") as f:
    f.write("我想我会一直孤单\n" "我支持你\n" "我理解你\n" "我爱你")

with open("note.txt", "r", encoding="utf-8") as f:
    note = f.read()
    print(note)

#普通写法
result = []
for i in range(5):
    result.append(i*2)
print(result)

#列表推导式
result = [i*2 for i in range(5)]
print(result)

#加条件
result = [i*2 for i in range(10) if i%2 == 0]
print(result)

tryone = [i for i in range(20) if i%3 == 0]
print(tryone)

#字符串批量去掉空格
lines = ["  i want to be with u", "  thank u next  "]
cleaned = [line.strip() for line in lines]
print(cleaned)

#普通列表
line1 = [i for i in range(10)]
#生成器
line2 = (i for i in range(20))
for i in line2:
    print(i)

#装饰器
import time

def my_timer(func):
    def wrapper():
        start = time.time()
        func()
        end = time.time()
        print(f"运行耗时：{end - start}秒")
    return wrapper


@my_timer
def say_hello():
    print("你好")

say_hello()


