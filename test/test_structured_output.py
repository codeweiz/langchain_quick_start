from typing import Optional, Union

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing_extensions import TypedDict, Annotated

from common.llm.deepseek import get_deepseek_chat_model


# 结构化输出

# 测试 with_structured_output 方法，用 Pydantic class 实现，底层是 PydanticToolsParser
# 除了 Pydantic 类的结构之外，Pydantic 类的名称、文档字符串以及参数的名称和提供的描述也非常重要
# 大多数情况下，with_structured_output 使用的是模型的函数 / 工具调用 API，可以将所有这些信息有效地视为添加到模型提示中
def test_with_structured_output_pydantic():
    model = get_deepseek_chat_model()

    # 使用 with_structured_output 方法将输出格式化为 Joke 类型，并按 Joke 类型属性的 description 约束或生成输出
    structured_llm = model.with_structured_output(Joke)
    response = structured_llm.invoke("Tell me a joke about dogs in Chinese")
    print(f"\nresponse: {response}")


# 测试 with_structured_output 方法，用 TypedDict 实现，底层是 JsonOutputKeyToolsParser
def test_with_structured_output_typeddict():
    model = get_deepseek_chat_model()

    # 使用 with_structured_output 方法将输出格式化为 Joke2 类型，并按 Joke2 类型属性的 description 约束或生成输出
    structured_llm = model.with_structured_output(Joke2)
    response = structured_llm.invoke("Tell me a joke about dogs in Chinese")
    print(f"\nresponse: {response}")


# 测试 with_structured_output 方法，用 JSON Schema 实现，底层是 JsonOutputKeyToolsParser
def test_with_structured_output_json_schema():
    model = get_deepseek_chat_model()

    # 自定义 JSON Schema
    json_schema = {
        "title": "joke",
        "description": "Joke to tell user.",
        "type": "object",
        "properties": {
            "setup": {
                "type": "string",
                "description": "The setup of the joke",
            },
            "punchline": {
                "type": "string",
                "description": "The punchline to the joke",
            },
            "rating": {
                "type": "integer",
                "description": "How funny the joke is, from 1 to 10",
                "default": None,
            },
        },
        "required": ["setup", "punchline"],
    }

    # 使用 with_structured_output 方法将输出格式化为 JSON Schema，并按 JSON Schema 属性的 description 约束或生成输出
    structured_llm = model.with_structured_output(json_schema)
    response = structured_llm.invoke("Tell me a joke about dogs in Chinese")
    print(f"\nresponse: {response}")


# 测试 with_structured_output 方法，用 Union 联合多个子类型，LLM 根据实际情况决定用何种方式返回，底层是 PydanticToolsParser
def test_with_structured_output_pydantic_union():
    model = get_deepseek_chat_model()

    # 使用 with_structured_output 方法将输出格式化为 FinalResponse 类型，并按 FinalResponse 类型属性的 description 约束或生成输出
    structured_llm = model.with_structured_output(FinalResponse)

    # Joke 类型
    response = structured_llm.invoke("Tell me a joke about dogs in Chinese.")
    print(f"\nresponse: {response}")

    # ConversationalResponse 类型返回
    response = structured_llm.invoke("How are you today?")
    print(f"\nresponse: {response}")


# 测试 with_structured_output 方法，用 Union 联合多个子类型，LLM 根据实际情况决定用何种方式返回，底层是 JsonOutputKeyToolsParser
def test_with_structured_output_typeddict_union():
    model = get_deepseek_chat_model()

    # 使用 with_structured_output 方法将输出格式化为 FinalResponse2 类型，并按 FinalResponse2 类型属性的 description 约束或生成输出
    structured_llm = model.with_structured_output(FinalResponse2)

    # Joke2 类型
    response = structured_llm.invoke("Tell me a joke about dogs in Chinese.")
    print(f"\nresponse: {response}")

    # ConversationalResponse2 类型返回
    response = structured_llm.invoke("How are you today?")
    print(f"\nresponse: {response}")


# 当输出类型为字典时（即架构指定为 TypedDict 类或 JSON Schema 字典时），才可以从结构化模型中流式输出
# 测试 with_structured_output 方法，用 TypedDict 实现，底层是 JsonOutputKeyToolsParser，流式输出
def test_with_structured_output_typeddict_stream():
    model = get_deepseek_chat_model()

    # 使用 with_structured_output 方法将输出格式化为 Joke2 类型，并按 Joke2 类型属性的 description 约束或生成输出
    structured_llm = model.with_structured_output(Joke2)

    # 流式输出，生成的内容已经是聚合后的块，而不是增量
    for chunk in structured_llm.stream("Tell me a joke about dogs in Chinese"):
        print(chunk)


# 测试 with_structured_output 方法，用 few shot 实现
def test_with_structured_output_few_shot():
    model = get_deepseek_chat_model()
    structured_llm = model.with_structured_output(Joke)
    system = """
            You are a hilarious comedian. Your specialty is knock-knock jokes. \
            Return a joke which has the setup (the response to "Who's there?") and the final punchline (the response to "<setup> who?").
            
            Here are some examples of jokes:
            
            example_user: Tell me a joke about planes
            example_assistant: {{"setup": "Why don't planes ever get tired?", "punchline": "Because they have rest wings!", "rating": 2}}
            
            example_user: Tell me another joke about planes
            example_assistant: {{"setup": "Cargo", "punchline": "Cargo 'vroom vroom', but planes go 'zoom zoom'!", "rating": 10}}
            
            example_user: Now about caterpillars
            example_assistant: {{"setup": "Caterpillar", "punchline": "Caterpillar really slow, but watch me turn into a butterfly and steal the show!", "rating": 5}}
            """
    prompt: ChatPromptTemplate = ChatPromptTemplate.from_messages([
        ("system", system),
        ("human", "{input}")
    ])

    few_shot_structured_llm = prompt | structured_llm
    response = few_shot_structured_llm.invoke({"input": "What's something funny about 程序员"})
    print(f"\nresponse: {response}")


# 高级特性，method 指定为 json_mode，并且在 prompt 中明确用某 key 响应
def test_with_structured_output_method():
    model = get_deepseek_chat_model()
    structured_llm = model.with_structured_output(None, method="json_mode")
    response = structured_llm.invoke("Tell me a joke about cats, respond in JSON with `setup` and `punchline` keys")
    print(f"\nresponse: {response}")


# 高级特性，include_raw 指定为 True，避免 LLM 在输出上引发异常，并自行处理原始输出
# response: {'raw': AIMessage(content='', additional_kwargs={'tool_calls': [{'id': 'call_0_01a72cba-78b0-40b7-b900-4f82bda0eb2a', 'function': {'arguments': '{"setup":"Why did the cat sit on the computer?","punchline":"Because it wanted to keep an eye on the mouse!","rating":7}', 'name': 'Joke'}, 'type': 'function', 'index': 0}], 'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 45, 'prompt_tokens': 206, 'total_tokens': 251, 'completion_tokens_details': None, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 192}, 'prompt_cache_hit_tokens': 192, 'prompt_cache_miss_tokens': 14}, 'model_name': 'deepseek-chat', 'system_fingerprint': 'fp_8802369eaa_prod0425fp8', 'id': '27d66ec3-0367-4a6b-8193-45695678a2e4', 'service_tier': None, 'finish_reason': 'tool_calls', 'logprobs': None}, id='run--5e764dae-bc58-4622-a8ca-9bf1943a7aec-0', tool_calls=[{'name': 'Joke', 'args': {'setup': 'Why did the cat sit on the computer?', 'punchline': 'Because it wanted to keep an eye on the mouse!', 'rating': 7}, 'id': 'call_0_01a72cba-78b0-40b7-b900-4f82bda0eb2a', 'type': 'tool_call'}], usage_metadata={'input_tokens': 206, 'output_tokens': 45, 'total_tokens': 251, 'input_token_details': {'cache_read': 192}, 'output_token_details': {}}), 'parsed': Joke(setup='Why did the cat sit on the computer?', punchline='Because it wanted to keep an eye on the mouse!', rating=7), 'parsing_error': None}
def test_with_structured_output_raw():
    model = get_deepseek_chat_model()
    structured_llm = model.with_structured_output(Joke, include_raw=True)
    response = structured_llm.invoke("Tell me a joke about cats")
    print(f"\nresponse: {response}")


# 笑话，Pydantic 实现
class Joke(BaseModel):
    # 开始
    setup: str = Field(description="The setup of the joke")

    # 亮点
    punchline: str = Field(description="The punchline to the joke")

    # 打分，1 到 10
    rating: Optional[int] = Field(default=None, description="How funny the joke is, from 1 to 10")


# 对话响应，Pydantic 实现
class ConversationalResponse(BaseModel):
    response: str = Field(description="A conversational response to the user's query")


# 最终响应，Pydantic 实现
class FinalResponse(BaseModel):
    final_output: Union[Joke, ConversationalResponse]


# 笑话，TypedDict 实现
class Joke2(TypedDict):
    setup: Annotated[str, ..., "The setup of the joke"]
    punchline: Annotated[str, ..., "The punchline to the joke"]
    rating: Annotated[Optional[int], None, "How funny the joke is, from 1 to 10"]


# 对话响应，TypedDict 实现
class ConversationalResponse2(TypedDict):
    response: Annotated[str, ..., "A conversational response to the user's query"]


# 最终响应，TypedDict 实现
class FinalResponse2(TypedDict):
    final_output: Union[Joke2, ConversationalResponse2]
