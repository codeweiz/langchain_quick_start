from langchain_community.cache import SQLiteCache
from langchain_core.caches import InMemoryCache
from langchain_core.globals import set_llm_cache

from core.llm.deepseek import get_deepseek_chat_model


# 测试聊天模型缓存：用内存缓存实现
def test_chat_model_caching_in_memory_cache():
    model = get_deepseek_chat_model()

    set_llm_cache(InMemoryCache())

    response = model.invoke("Tell me a joke")
    print(f"response: {response}")

    # LangSmith 0s 返回
    response = model.invoke("Tell me a joke")
    print(f"response: {response}")


# 测试聊天模型缓存：用 SQLiteCache 实现
def test_chat_model_caching_sqlite_cache():
    model = get_deepseek_chat_model()

    set_llm_cache(SQLiteCache(database_path=".langchain.db"))

    response = model.invoke("Tell me a joke")
    print(f"response: {response}")

    # LangSmith 0s 返回
    response = model.invoke("Tell me a joke")
    print(f"response: {response}")
