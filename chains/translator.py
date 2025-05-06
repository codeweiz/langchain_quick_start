from langchain.chat_models import init_chat_model
from langchain_core.messages import BaseMessage
from langchain_core.prompt_values import PromptValue
from langchain_core.prompts import ChatPromptTemplate

# 初始化 LLM
model = init_chat_model("deepseek-chat", model_provider="deepseek")

# 初始化提示词模板
system_template = "You are a language expert, now just translate the following from {source_language} into {target_language}, do not give any other info or notes"
prompt_template: ChatPromptTemplate = ChatPromptTemplate.from_messages([
    ("system", system_template),
    ("user", "{text}")
])


# 翻译
def translate(source_language: str, target_language: str, text: str, ) -> BaseMessage:
    # 生成提示词
    prompt: PromptValue = prompt_template.invoke(
        {"source_language": source_language, "target_language": target_language, "text": text}
    )

    # LLM 调用
    result: BaseMessage = model.invoke(prompt.to_messages())
    return result
