from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import InMemoryVectorStore

from core.embeddiings.huggingface_embedding import get_huggingface_embedding


# 获取 huggingface embedding 的基于内存的向量数据库
def get_in_memory_vector_store() -> InMemoryVectorStore:
    embedding: Embeddings = get_huggingface_embedding()
    return InMemoryVectorStore(embedding)
