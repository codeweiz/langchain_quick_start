from common.llm.deepseek import get_deepseek_chat_model


# 测试获取对数概率
def test_logprobs():
    model = get_deepseek_chat_model()
    model.bind(logprobs=True)

    # DeepSeek Chat Model 不支持 logprobs
    # OPENAI Chat Model 支持
    response = model.invoke(("human", "how are you today"))
    logprobs = response.response_metadata["logprobs"]
    print(f"logprobs: {logprobs}")
