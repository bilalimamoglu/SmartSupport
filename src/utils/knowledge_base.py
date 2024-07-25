# src/utils/knowledge_base.py

import os
import logging
from langchain.chat_models import ChatOpenAI
from langchain_community.document_loaders import TextLoader
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAI
from src.config.config import Config
from src.config.constants import DEFAULT_MODEL
from src.utils.logger import setup_logger

# Setup logger
logger = setup_logger(__name__)

async def load_sales_doc_vector_store(file_name: str):
    """
    Load a vector store for sales documents from a given file.

    :param file_name: The name of the file containing sales documents.
    :return: A FAISS vector store containing the documents.
    """
    fullpath = os.path.join(Config.PROJECT_ROOT, 'data', 'knowledge', file_name)
    logger.info(f"Loading documents from {fullpath}")
    loader = TextLoader(fullpath)
    docs = loader.load()
    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    logger.info(f"Splitting documents into chunks of 1000 characters")
    new_docs = splitter.split_documents(docs)
    logger.info("Creating vector store from documents")
    return FAISS.from_documents(new_docs, OpenAIEmbeddings())

async def setup_knowledge_base(file_name: str, llm: OpenAI):
    """
    Set up the knowledge base for a given file and language model.

    :param file_name: The name of the file containing knowledge base data.
    :param llm: The language model instance.
    :return: A RetrievalQA instance for querying the knowledge base.
    """
    logger.info(f"Setting up knowledge base for {file_name}")
    vector_store = await load_sales_doc_vector_store(file_name)
    logger.info("Creating RetrievalQA from vector store")
    llm = ChatOpenAI(model_name=DEFAULT_MODEL)
    return  RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=vector_store.as_retriever())

async def get_tools(product_catalog: str):
    """
    Initialize tools for product catalog management.

    :param product_catalog: The file name of the product catalog.
    :return: A list of tools for managing the product catalog.
    """
    logger.info(f"Initializing tools for product catalog {product_catalog}")
    chain = await setup_knowledge_base(product_catalog, OpenAI(api_key=Config.OPENAI_API_KEY))
    tools = [
        {
            "name": "ProductSearch",
            "description": "Useful for answering questions about product information.",
            "chain": chain,
        }
    ]
    logger.info("Tools setup complete")
    return tools
