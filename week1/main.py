from chat_client import create_client, get_ai_reply

def main():
    client = create_client()
    messages = [
        {"role": "system","content": "你是一个很有帮助的AI助手"}
    ]

    while True:
        user_input = input("user:")
        if user_input =="exit":
            print("离开")
            break

        if user_input.strip() == "":
            print("请输入内容：")
            continue

        messages.append({"role": "user", "content":user_input})
        ai_reply = get_ai_reply(client=client, messages=messages)
        print("AI:" + ai_reply)

        if not ai_reply.startswith("错误:"):
            messages.append({"role":"assistant", "content":ai_reply})

if __name__ == "__main__":
    main()