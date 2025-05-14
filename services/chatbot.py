from langchain_core.prompt_values import PromptValue
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import START
from langgraph.graph import StateGraph, MessagesState
from langgraph.graph.state import CompiledStateGraph

from common.llm.deepseek import get_deepseek_chat_model


# 获取聊天机器人
def get_chat_bot() -> CompiledStateGraph:
    # Chat Model
    model = get_deepseek_chat_model()

    # prompt
    prompt_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You talk like a princess. Answer all questions to the best of your ability."
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    # 定义一个 graph
    workflow = StateGraph(state_schema=MessagesState)

    # 调用模型的方法
    def call_model(state: MessagesState):
        prompt_value: PromptValue = prompt_template.invoke(state)
        response = model.invoke(prompt_value)
        return {"messages": response}

    # 在 graph 中添加一个单独 node
    workflow.add_edge(START, "model")
    workflow.add_node("model", call_model)

    # 添加记录
    memory = MemorySaver()
    chatbot_app: CompiledStateGraph = workflow.compile(checkpointer=memory)
    return chatbot_app
