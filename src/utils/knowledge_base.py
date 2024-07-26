# src/utils/knowledge_base.py

import os
import logging
from langchain_community.document_loaders import TextLoader
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAI
from src.config.config import Config
from src.utils.logger import setup_logger
from src.config.constants import DEFAULT_MODEL
from src.utils.extraction_tool import ExtractionTool

# Setup logger
logger = setup_logger(__name__)


def load_sales_doc_vector_store(file_name: str):
    fullpath = os.path.join(Config.PROJECT_ROOT, 'data', 'knowledge', file_name)
    logger.info(f"Loading documents from {fullpath}")
    loader = TextLoader(fullpath)
    docs = loader.load()
    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    logger.info(f"Splitting documents into chunks of 1000 characters")
    new_docs = splitter.split_documents(docs)
    logger.info("Creating vector store from documents")
    return FAISS.from_documents(new_docs, OpenAIEmbeddings())


def setup_knowledge_base(file_name: str, llm: OpenAI):
    logger.info(f"Setting up knowledge base for {file_name}")
    vector_store = load_sales_doc_vector_store(file_name)
    logger.info("Creating RetrievalQA from vector store")
    return RetrievalQA.from_chain_type(OpenAI(api_key=Config.OPENAI_API_KEY, model=DEFAULT_MODEL),
                                       retriever=vector_store.as_retriever())


async def get_tools(product_catalog: str):
    logger.info(f"Initializing tools for product catalog {product_catalog}")
    chain = setup_knowledge_base(product_catalog, OpenAI(api_key=Config.OPENAI_API_KEY, model=DEFAULT_MODEL))
    tools = [
        {
            "name": "ProductSearch",
            "description": "Useful for answering questions about product information.",
            "chain": chain,
        }
    ]

    # Include extraction tool if needed
    extraction_tool = ExtractionTool()
    tools.append({
        "name": "ExtractInfo",
        "description": "Useful for extracting name and contact information from the conversation.",
        "tool": extraction_tool
    })

    logger.info("Tools setup complete")
    return tools
