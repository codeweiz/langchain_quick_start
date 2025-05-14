from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate

from common.llm.deepseek import get_deepseek_chat_model


# 使用 提示模板 和 聊天模型 构建一个简单的大语言模型应用程序

# 测试加载模型
def test_get_deepseek_chat_model():
    model = get_deepseek_chat_model()

    # 校验模型加载成功
    assert model is not None


# 校验模型 invoke
def test_chat_model_invoke():
    model = get_deepseek_chat_model()

    # 校验模型可以 invoke 普通 str
    result: BaseMessage = model.invoke("中国的首都是哪里？不需要介绍")
    print(result.content)


# 校验模型 invoke 翻译
def test_chat_model_invoke_translate():
    model = get_deepseek_chat_model()

    messages = [
        SystemMessage(
            "Translate the following from Chinese into English, do not mention any other notes or descriptions"),
        HumanMessage("你好，请问食堂怎么走？")
    ]

    result: BaseMessage = model.invoke(messages)
    print(result.content)


# 校验模型 invoke
def test_chat_model_invoke2():
    model = get_deepseek_chat_model()
    print('\n' + model.invoke("Hello One").content)
    print('\n' + model.invoke([{"role": "user", "content": "Hello Two"}]).content)
    print('\n' + model.invoke([HumanMessage("Hello Three")]).content)


# 校验模型 stream
def test_chat_model_invoke_stream():
    model = get_deepseek_chat_model()
    messages = [
        SystemMessage(
            "Translate the following from Chinese into English, do not mention any other notes or descriptions"),
        HumanMessage("你好，请问食堂怎么走？")
    ]
    for token in model.stream(messages):
        print(token.content, end="|")


# 校验提示词模板
def test_prompt_template():
    model = get_deepseek_chat_model()
    system_template = "Translate the following from Chinese into {language}"

    # ChatPromptTemplate 根据 messages 生成提示词模板
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_template),
        ("user", "{text}")
    ])

    # 提示词模板 + 占位符对应的值，生成具体提示词
    prompt = prompt_template.invoke({"language": "English", "text": "这是一段翻译文本"})

    # LLM 调用生成的提示词
    response: BaseMessage = model.invoke(prompt)
    print('\n' + response.content)
