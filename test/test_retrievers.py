from typing import List

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_core.runnables import chain
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

from common.embeddings.huggingface_embedding import get_huggingface_embedding


# 使用文档加载器、嵌入模型和向量数据库，基于 PDF 构建一个语义搜索引擎

# 测试 Document
def test_document():
    documents = [
        Document(
            page_content="Dogs are great companions, known for their loyalty and friendliness.",
            metadata={"source": "mammal-pets-doc"}
        ),
        Document(
            page_content="Cats are independent pets that often enjoy their own space.",
            metadata={"source": "mammal-pets-doc"}
        )
    ]


# 校验文档加载器 document loader
def test_document_loader():
    file_path = "resources/nke-10k-2023.pdf"

    # PyPDFLoader 加载指定路径的 PDF 文件，返回文档加载器
    loader = PyPDFLoader(file_path)
    # 加载器调用 load 方法进行加载，将 PDF 每页数据存为一个 Document，返回 list[Document]
    docs: list[Document] = loader.load()

    # PDF 一共 107 页，这里 docs 也有 107 个 Document
    print(f"\n{len(docs)}\n")
    # 打印第一页的 0 到 200 个字符
    print(f"{docs[0].page_content[:200]}\n")
    # 打印第一页的 metadata 原数据，有 source（来源）和 page（当前页码）
    print(f"{docs[0].metadata}\n")


# 校验文本分割器
def test_text_split():
    file_path = "resources/nke-10k-2023.pdf"

    loader = PyPDFLoader(file_path)
    docs: list[Document] = loader.load()

    # 递归字符文本分割器
    # 把文档分为 1000 个块
    # 块与块之间有 200 个字符重叠
    # add_start_index=True，拆分后的文档在初始文档中开始的字符索引作为数据属性 start_index 保留下来
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200, add_start_index=True
    )

    # 拆分 PDF 文档，返回 List[Document]，107 拆分为 516
    all_splits: List[Document] = text_splitter.split_documents(docs)
    print(f"\n{len(all_splits)}\n")


# 测试嵌入：文本转为向量
def test_embedding():
    file_path = "resources/nke-10k-2023.pdf"
    loader = PyPDFLoader(file_path)
    docs: list[Document] = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, add_start_index=True)
    all_splits: List[Document] = text_splitter.split_documents(docs)

    # huggingface embedding 768 维
    # vector 这种数据结构支持高效的相似度搜索
    embedding = get_huggingface_embedding()
    vector_1: List[float] = embedding.embed_query(all_splits[0].page_content)
    vector_2: List[float] = embedding.embed_query(all_splits[1].page_content)

    assert len(vector_1) == len(vector_2)
    print(f"\n{len(vector_1)}")


# 测试向量数据库
def test_vector_store():
    file_path = "resources/nke-10k-2023.pdf"
    loader = PyPDFLoader(file_path)
    docs: list[Document] = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, add_start_index=True)
    all_splits: List[Document] = text_splitter.split_documents(docs)
    embedding = get_huggingface_embedding()

    # 使用内存向量数据库
    vector_store = InMemoryVectorStore(embedding)
    # 向量数据库添加文档，返回索引
    ids: list[str] = vector_store.add_documents(documents=all_splits)
    print(f"\n{ids}")

    # 相似度查询
    results: list[Document] = vector_store.similarity_search("How many distribution centers does Nike have in the US?")
    print(f"\n{results[0]}")

    # 带分数的相似度查询
    results: list[tuple[Document, float]] = vector_store.similarity_search_with_score(
        "What was Nike's revenue in 2023?"
    )
    doc, score = results[0]
    print(f"\nScore: {score}\n{doc}")

    # 根据与嵌入查询的相似度返回文档，测试下来，最为准确
    embeddings = embedding.embed_query("How were Nike's margins impacted in 2023?")
    results: list[Document] = vector_store.similarity_search_by_vector(embeddings)
    print(f"\n{results[0]}")


# 测试检索器
def test_retrievers():
    file_path = "resources/nke-10k-2023.pdf"
    loader = PyPDFLoader(file_path)
    docs: list[Document] = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, add_start_index=True)
    all_splits: List[Document] = text_splitter.split_documents(docs)
    embedding = get_huggingface_embedding()
    vector_store = InMemoryVectorStore(embedding)
    vector_store.add_documents(documents=all_splits)

    # 定义一个基于向量数据库相似度查询的检索器
    @chain
    def retriever(query: str) -> List[Document]:
        return vector_store.similarity_search(query, k=1)

    # 检索器批量查询
    result = retriever.batch(
        [
            "How many distribution centers does Nike have in the US?",
            "What was Nike incorporated?",
        ]
    )
    print(f"\n{result}")

    # 向量数据库也可以通过 as_retriever 方法生成一个检索器
    # search_type 支持 similarity（默认、相似性）、mmr（上文所述的最大边际相关性）、similarity_score_threshold（相似度得分阈值）
    vector_store.as_retriever(search_type="similarity", search_kwargs={'k': 1})
    result = retriever.batch(
        [
            "How many distribution centers does Nike have in the US?",
            "What was Nike incorporated?",
        ]
    )
    print(f"\n{result}")

    # 检索器可以轻松集成到更复杂的应用程序中，例如检索增强生成（RAG）应用程序
    # 这些应用程序将给定的问题与检索到的上下文结合起来，形成大语言模型（LLM）的提示
