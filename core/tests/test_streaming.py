from typing import List

import pytest
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessageChunk
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from core.llm.deepseek import get_deepseek_chat_model


# 测试流式输出
def test_stream():
    model: BaseChatModel = get_deepseek_chat_model()

    chunks = []
    for chunk in model.stream("What color is the sky?"):
        chunks.append(chunk)
        print(chunk.content, end="|", flush=True)


# 测试异步流式输出
@pytest.mark.asyncio
async def test_async_stream():
    model: BaseChatModel = get_deepseek_chat_model()

    chunks: List[AIMessageChunk] = []
    async for chunk in model.astream("What color is the sky?"):
        chunks.append(chunk)
        print(chunk.content, end="|", flush=True)
    print(f"\nchunks[0]: {chunks[0]}")

    # AIMessageChunk，支持累加
    print(f"\nchunks[0 - 4]: {chunks[0] + chunks[1] + chunks[2] + chunks[3] + chunks[4]}")


# 测试 Chain 的流式输出
@pytest.mark.asyncio
async def test_chain_stream():
    model: BaseChatModel = get_deepseek_chat_model()
    prompt: ChatPromptTemplate = ChatPromptTemplate.from_template("tell me a joke about {topic}")
    parser: StrOutputParser = StrOutputParser()

    chain = prompt | model | parser

    async for chunk in chain.astream({"topic": "dogs"}):
        print(chunk, end="|", flush=True)
