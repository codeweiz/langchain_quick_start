from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage

# 初始化 chat model
model = init_chat_model("deepseek-chat", model_provider="deepseek")

# 构造聊天信息
messages = [
    HumanMessage(content="Hi! I'm Bob"),
    AIMessage(content="Hello Bob! How can I assist you today?"),
    HumanMessage(content="What is my name?")
]


# 聊天
def chat() -> BaseMessage:
    return model.invoke(messages)
