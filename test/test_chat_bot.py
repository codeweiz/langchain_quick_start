from langchain_core.messages import HumanMessage

from services.chatbot import get_chat_bot


# 测试聊天机器人
def test_chat_bot():
    chat_bot_app = get_chat_bot()

    config = {"configurable": {"thread_id": "abc345"}}

    query = "Hi, I'm Jim."
    input_messages = [HumanMessage(content=query)]
    output = chat_bot_app.invoke({"messages": input_messages}, config)
    output["messages"][-1].pretty_print()

    query = "What's my name?"
    input_messages = [HumanMessage(content=query)]
    output = chat_bot_app.invoke({"messages": input_messages}, config)
    output["messages"][-1].pretty_print()
