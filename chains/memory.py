from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import START
from langgraph.graph import StateGraph, MessagesState

# 初始化 chat model
model = init_chat_model("deepseek-chat", model_provider="deepseek")

# 定义一个 state graph
workflow: StateGraph = StateGraph(state_schema=MessagesState)


# 定义一个函数，可以调用这个模型
def call_model(state: MessagesState):
    response = model.invoke(state["messages"])
    return {"messages": response}


# 定义 graph 中的点和边
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

# 添加 memory
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)


def memory_chat(query: str):
    config = {"configurable": {"thread_id": "abc123"}}
    input_messages = [HumanMessage(query)]
    output = app.invoke({"messages": input_messages}, config)
    output["messages"][-1].pretty_print()
