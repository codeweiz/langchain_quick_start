from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.output_parsers import PydanticToolsParser
from langchain_core.tools import tool
from pydantic import BaseModel, Field

from core.llm.deepseek import get_deepseek_chat_model


# 加法，Pydantic 实现
class AddByPydantic(BaseModel):
    a: int = Field(..., description="First integer")
    b: int = Field(..., description="Second integer")


# 乘法，Pydantic 实现
class MultiplyByPydantic(BaseModel):
    a: int = Field(..., description="First integer")
    b: int = Field(..., description="Second integer")


# 测试工具调用
def test_tool_calling():
    model = get_deepseek_chat_model()
    tools = [AddByPydantic, MultiplyByPydantic]
    llm_with_tools = model.bind_tools(tools)
    query_str = "What is 3 * 12?"
    response = llm_with_tools.invoke(query_str)
    print(f"response: {response}")


# 测试解析
def test_tool_calling_parsing():
    model = get_deepseek_chat_model()
    tools = [AddByPydantic, MultiplyByPydantic]
    llm_with_tools = model.bind_tools(tools)

    chain = llm_with_tools | PydanticToolsParser(tools=tools)
    query_str = "What is 3 * 12? Also, what is 11 + 49?"

    # 结果：[MultiplyByPydantic(a=3, b=12), AddByPydantic(a=11, b=49)]
    response = chain.invoke(query_str)
    print(f"response: {response}")


# 使用@tool装饰器时，被装饰的函数必须有文档字符串(docstring)或者提供描述

# 加法
@tool
def add(a: int, b: int) -> int:
    """Adds a and b."""
    return a + b


# 乘法
@tool
def multiply(a: int, b: int) -> int:
    """Multiplies a and b."""
    return a * b


# 测试工具调用的结果返回给模型
def test_tool_results_pass_to_model():
    model = get_deepseek_chat_model()
    tools = [add, multiply]
    llm_with_tools = model.bind_tools(tools)

    query_str = "What is 3 * 12? Also, what is 11 + 49?"
    messages = [HumanMessage(content=query_str)]

    # 第一次调用模型获取工具调用，获取 AI Message
    ai_msg = llm_with_tools.invoke(messages)
    messages.append(ai_msg)

    # 对于 AI Message 中的 tool_call，只要匹配上 tool，就 invoke 调用，并把调用后的结果也存入 messages 中
    for tool_call in ai_msg.tool_calls:
        tool_name = tool_call["name"].lower()
        selected_tool = {"add": add, "multiply": multiply}[tool_name]

        # tool invoke tool_call
        tool_msg = selected_tool.invoke(tool_call)
        messages.append(tool_msg)
    print(f"\nmessages: {messages}")

    # 使用更新后的消息历史再次调用模型，总结答案
    response = llm_with_tools.invoke(messages)
    print(f"\nresponse: {response}")
