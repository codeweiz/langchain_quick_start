from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import START
from langgraph.graph import StateGraph, MessagesState
from common.llm.deepseek import get_deepseek_chat_model

model = get_deepseek_chat_model()
workflow: StateGraph = StateGraph(state_schema=MessagesState)

def call_model(state: MessagesState):
    """
    调用模型，返回 AI 回复。
    :param state: 消息状态
    :return: AI 回复消息
    """
    response = model.invoke(state["messages"])
    return {"messages": response}

workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

def memory_chat(query: str) -> None:
    """
    记忆对话，打印 AI 回复。
    :param query: 用户输入
    """
    config = {"configurable": {"thread_id": "abc123"}}
    input_messages = [HumanMessage(query)]
    output = app.invoke({"messages": input_messages}, config)
    output["messages"][-1].pretty_print() 