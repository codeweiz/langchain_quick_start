from langchain_core.messages import BaseMessage

from chains import translate


def main():
    result: BaseMessage = translate("Chinese", "English", "衬衫的价格是九磅十五便士")
    print(result.content)


if __name__ == "__main__":
    main()
