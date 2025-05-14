import json
import re
from typing import List

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from common.llm.deepseek import get_deepseek_chat_model


# 结构化输出、高级特性 PydanticOutputParser、custom parser

# 使用 PydanticOutputParser，用 Pydantic class 实现
def test_with_structured_output_parser():
    model: BaseChatModel = get_deepseek_chat_model()
    parser: PydanticOutputParser = PydanticOutputParser(pydantic_object=People)
    prompt: ChatPromptTemplate = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Answer the user query. Wrap the output in `json` tags\n{format_instructions}"
            ),
            (
                "human",
                "{query}"
            )
        ]
    ).partial(format_instructions=parser.get_format_instructions())
    query_str: str = "Anna is 23 years old and she is 6 feet tall"

    # 提示词、LLM、解析器
    chain = prompt | model | parser
    response = chain.invoke({"query": query_str})
    print(f"response: {response}")


# 使用自定义解析器
def test_with_structured_output_parser_custom():
    model: BaseChatModel = get_deepseek_chat_model()
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Answer the user query. Output your answer as JSON that  "
                "matches the given schema: \`\`\`json\n{schema}\n\`\`\`. "
                "Make sure to wrap the answer in \`\`\`json and \`\`\` tags",
            ),
            ("human", "{query}"),
        ]
    ).partial(schema=People.model_json_schema())

    query_str = "Anna is 23 years old and she is 6 feet tall"

    print(prompt.format_prompt(query=query_str).to_string())

    chain = prompt | model | extract_json

    response = chain.invoke({"query": query_str})
    print(f"response: {response}")


# 自定义解析器
def extract_json(message: AIMessage) -> List[dict]:
    text = message.content
    pattern = r"\`\`\`json(.*?)\`\`\`"

    matches = re.findall(pattern, text, re.DOTALL)

    try:
        return [json.loads(match.strip()) for match in matches]
    except Exception:
        raise ValueError(f"Failed to extract json from {message}")


# Person，Pydantic 实现
class Person(BaseModel):
    name: str = Field(..., description="The name of the person")
    height_in_meters: float = Field(..., description="The height of the person expressed in meters")


# People，Pydantic 实现
class People(BaseModel):
    people: List[Person]
