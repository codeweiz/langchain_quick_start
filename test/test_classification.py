from langchain_core.language_models import BaseChatModel
from langchain_core.prompt_values import PromptValue
from langchain_core.prompts import ChatPromptTemplate

from common.classification import Classification, FinerClassification
from common.llm.deepseek import get_deepseek_chat_model


# 文本分类与结构化输出

# 测试文本分类与结构化输出
def test_classification():
    # 获取 deepseek chat LLM
    model: BaseChatModel = get_deepseek_chat_model()

    # 提示词模板：从以下段落中提取所需信息，仅提取 “Classification” 函数中提到的属性
    tagging_prompt_template: ChatPromptTemplate = ChatPromptTemplate.from_template(
        """
        Extract the desired information from the following passage.
        Only extract the properties mentioned in the 'Classification' function.
        Passage:
        {input}
        """
    )

    # 将 LLM 的输出结构化为 Classification
    structured_llm = model.with_structured_output(Classification)

    # 提示词输入
    inp = "Estoy increiblemente contento de haberte conocido! Creo que seremos muy buenos amigos!"

    # 提示词模板生成提示词
    prompt = tagging_prompt_template.invoke({"input": inp})

    # 结构化的 LLM 调用提示词
    response = structured_llm.invoke(prompt)

    # 输出结果：sentiment='positive' aggressiveness=1 language='Spanish'
    print(f"\n{response}")

    # 输出结果转为字典：{'sentiment': 'positive', 'aggressiveness': 1, 'language': 'es'}
    print(response.model_dump())


# 校验更精细的文本分类
def test_finer_classification():
    # 获取 deepseek chat LLM
    model: BaseChatModel = get_deepseek_chat_model()

    # 提示词模板：从以下段落中提取所需信息，仅提取 “Classification” 函数中提到的属性
    tagging_prompt_template: ChatPromptTemplate = ChatPromptTemplate.from_template(
        """
        Extract the desired information from the following passage.
        Only extract the properties mentioned in the 'Classification' function.
        Passage:
        {input}
        """
    )

    # 将 LLM 的输出结构化为 FinerClassification
    structured_llm = model.with_structured_output(FinerClassification)

    # 提示词输入
    inp = "Estoy increiblemente contento de haberte conocido! Creo que seremos muy buenos amigos!"

    # 提示词模板生成提示词
    prompt: PromptValue = tagging_prompt_template.invoke({"input": inp})

    # 结构化的 LLM 调用提示词
    response = structured_llm.invoke(prompt)

    # 输出结果：sentiment='happy' aggressiveness=1 language='spanish'
    print(f"\n{response}")

    # 输出结果转为字典：{'sentiment': 'happy', 'aggressiveness': 1, 'language': 'spanish'}
    print(response.model_dump())
