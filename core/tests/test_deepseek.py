from langchain_core.messages import BaseMessage

from core.llm.deepseek import get_deepseek_chat_model


# 校验 deepseek 模型
def test_get_deepseek_chat_model():
    model = get_deepseek_chat_model()

    # 校验模型加载成功
    assert model is not None


# 校验模型 invoke
def test_chat_model_invoke():
    model = get_deepseek_chat_model()

    # 校验模型可以 invoke 普通 str
    message: BaseMessage = model.invoke("中国的首都是哪里？不需要介绍")
    print(message.content)
    assert message.content == '北京'
