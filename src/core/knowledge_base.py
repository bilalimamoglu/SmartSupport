import os
import logging
from openai import AsyncOpenAI
from langchain.document_loaders import TextLoader
from langchain.vectorstores import HNSWLib
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQAChain
from langchain.tools import ChainTool
from langchain.text_splitter import CharacterTextSplitter
from langchain_core.language_models.base import BaseLanguageModel
from langchain_openai import OpenAI
from src.config.config import Config
from src.utils.logger import setup_logger

# Setup logger
logger = setup_logger(__name__)

async def load_sales_doc_vector_store(file_name: str):
    fullpath = os.path.join(Config.PROJECT_ROOT, 'data', 'knowledge', file_name)
    logger.info(f"Loading documents from {fullpath}")
    loader = TextLoader(fullpath)
    docs = await loader.load()
    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    logger.info(f"Splitting documents into chunks of 1000 characters")
    new_docs = splitter.split_documents(docs)
    logger.info("Creating vector store from documents")
    return HNSWLib.from_documents(new_docs, OpenAIEmbeddings())

async def setup_knowledge_base(file_name: str, llm: BaseLanguageModel):
    logger.info(f"Setting up knowledge base for {file_name}")
    vector_store = await load_sales_doc_vector_store(file_name)
    logger.info("Creating RetrievalQAChain from vector store")
    return RetrievalQAChain.from_llm(llm, vector_store.as_retriever())

async def get_tools(product_catalog: str):
    logger.info(f"Initializing tools for product catalog {product_catalog}")
    chain = await setup_knowledge_base(product_catalog, OpenAI(api_key=Config.OPENAI_API_KEY))
    tools = [
        ChainTool(
            name="ProductSearch",
            description="Useful for answering questions about product information.",
            chain=chain,
        )
    ]
    logger.info("Tools setup complete")
    return tools
