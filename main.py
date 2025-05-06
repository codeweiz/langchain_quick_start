from langchain_core.messages import BaseMessage

from chains.memory import memory_chat
from chains.translator import translate
from chains.chatbot import chat


def main():
    # result: BaseMessage = translate("Chinese", "English", "衬衫的价格是九磅十五便士")
    # print(result.content)

    # result: BaseMessage = chat()
    # print(result.content)

    memory_chat("你好，我是 Bob")
    memory_chat("我的名字叫什么？")


if __name__ == "__main__":
    main()
