from services.memory import memory_chat


def main():
    memory_chat("你好，我是 Bob")
    memory_chat("我的名字叫什么？")


if __name__ == "__main__":
    main()
