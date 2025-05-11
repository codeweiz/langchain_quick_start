from typing import List

from langchain_core.documents import Document
from langchain_core.runnables import chain
from langchain_core.vectorstores import VectorStore

from core.vector_stores.in_memory_vector_store import get_in_memory_vector_store


# 自定义检索器，基于向量数据库相似度查询
@chain
def similarity_retriever(query: str) -> List[Document]:
    vector_store: VectorStore = get_in_memory_vector_store()
    return vector_store.similarity_search(query, k=1)
