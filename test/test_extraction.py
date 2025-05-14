from langchain_core.language_models import BaseChatModel
from langchain_core.prompt_values import PromptValue
from langchain_core.prompts import ChatPromptTemplate

from common.classification.person import Person, PersonList
from common.llm.deepseek import get_deepseek_chat_model


# 使用聊天模型和少样本示例从文本和其他非结构化媒体中提取结构化数据。

# 测试文本抽取
def test_extraction():
    model: BaseChatModel = get_deepseek_chat_model()
    prompt_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an expert extraction algorithm. Only extract relevant information from the text. If you do not know the value of an attribute asked to extract, return null for the attribute's value.",
            ),
            (
                "human",
                "{text}"
            )
        ]
    )

    # 从文本中提取单个 Person
    structure_llm = model.with_structured_output(schema=Person)
    text = "张三长大了，现在都一米八了，还有一头乌黑的头发。"
    prompt: PromptValue = prompt_template.invoke({"text": text})
    response = structure_llm.invoke(prompt)
    print(f"\nresponse: {response}")

    # 从文本中提取多个 Person
    structure_llm = model.with_structured_output(schema=PersonList)
    text = "My name is Jeff, my hair is black and I'm 6 feet tall. Anna has the same color hair as me."
    prompt: PromptValue = prompt_template.invoke({"text": text})
    response = structure_llm.invoke(prompt)
    print(f"\nresponse: {response}")
