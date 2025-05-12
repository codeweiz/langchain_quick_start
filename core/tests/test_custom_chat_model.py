import pytest
from langchain_core.messages import HumanMessage, AIMessage

from core.llm.chat_parrot_link import ChatParrotLink


# 测试自定义聊天模型
def test_custom_chat_model():
    model = ChatParrotLink(parrot_buffer_length=3, model="my_custom_model")

    response = model.invoke([
        HumanMessage(content="hello!"),
        AIMessage(content="Hi there human!"),
        HumanMessage(content="Meow!")
    ])

    print(f"\nresponse: {response}")

    response = model.invoke("hello")
    print(f"\nresponse: {response}")

    response = model.batch(["hello", "goodbye"])
    print(f"\nresponse: {response}\n")

    for chunk in model.stream("cat"):
        print(chunk.content, end="|")


# 测试自定义 LLM 异步
@pytest.mark.asyncio
async def test_custom_chat_model_async():
    model = ChatParrotLink(parrot_buffer_length=3, model="my_custom_model")

    async for chunk in model.astream("cat"):
        print(chunk.content, end="|")

    async for event in model.astream_events("cat", version="v1"):
        print(event)
