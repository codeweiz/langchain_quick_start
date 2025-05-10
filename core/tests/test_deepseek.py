from core.llm.deepseek import get_deepseek_chat_model

def test_get_deepseek_chat_model():
    model = get_deepseek_chat_model()
    assert model is not None
    # 可根据实际模型类型进一步断言 