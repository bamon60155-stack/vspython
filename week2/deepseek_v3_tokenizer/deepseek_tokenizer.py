# pip3 install transformers
# python3 deepseek_tokenizer.py
import transformers

# chat_tokenizer_dir = "./"
chat_tokenizer_dir = "C:/Users/lenovo/Desktop/vspython/deepseek_v3_tokenizer/"


tokenizer = transformers.AutoTokenizer.from_pretrained( 
        chat_tokenizer_dir, trust_remote_code=True
        )

# result = tokenizer.encode("你好")
# print(result)
# print(tokenizer.encode("cat"))
# print(tokenizer.encode("understanding"))
# print(tokenizer.encode("internationalization"))
# print(tokenizer.encode("the"))
# print(tokenizer.encode("satellite"))
# print(tokenizer.encode("radiofrequency"))
# print(tokenizer.encode("I am studying satellite communication."))
print(tokenizer.encode("aaaaaaaaaa"))
for t in [43, 356, 68870, 1045, 268, 47491, 52511, 16]:
    print(t, tokenizer.decode([t]))
