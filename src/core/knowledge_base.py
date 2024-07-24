# src/core/knowledge_base.py

from openai import AsyncOpenAI
from langchain.document_loaders import TextLoader
from langchain.vectorstores import HNSWLib
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQAChain
from langchain.tools import ChainTool
from src.config.config import Config
import os

async def load_sales_doc_vector_store(file_name: str):
    fullpath = os.path.join(Config.PROJECT_ROOT, 'knowledge', file_name)
    loader = TextLoader(fullpath)
    docs = await loader.load()
    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    new_docs = await splitter.split_documents(docs)
    return await HNSWLib.from_documents(new_docs, OpenAIEmbeddings())

async def setup_knowledge_base(file_name: str, llm: BaseLanguageModel):
    vector_store = await load_sales_doc_vector_store(file_name)
    return RetrievalQAChain.from_llm(llm, vector_store.as_retriever())

async def get_tools(product_catalog: str):
    chain = await setup_knowledge_base(product_catalog, AsyncOpenAI(api_key=Config.OPENAI_API_KEY))
    tools = [
        ChainTool(
            name="ProductSearch",
            description="Useful for answering questions about product information.",
            chain=chain,
        )
    ]
    return tools
