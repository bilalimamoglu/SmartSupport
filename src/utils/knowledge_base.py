import os
import logging
from langchain_community.document_loaders import TextLoader
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAI
from langchain_openai import ChatOpenAI  # Use ChatOpenAI for chat models
from src.config.config import Config
from src.utils.logger import setup_logger
from src.config.constants import DEFAULT_MODEL

# Setup logger
logger = setup_logger(__name__)

def load_sales_doc_vector_store(file_name: str):
    """
    Load documents from a specified file, split them into chunks, and create a FAISS vector store.

    :param file_name: Name of the file containing the sales documents.
    :return: FAISS vector store.
    """
    fullpath = os.path.join(Config.PROJECT_ROOT, 'data', 'knowledge', file_name)
    logger.info(f"Loading documents from {fullpath}")
    loader = TextLoader(fullpath)
    docs = loader.load()
    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    logger.info("Splitting documents into chunks of 1000 characters")
    new_docs = splitter.split_documents(docs)
    logger.info("Creating vector store from documents")
    return FAISS.from_documents(new_docs, OpenAIEmbeddings())

def setup_knowledge_base(file_name: str, model_name: str = DEFAULT_MODEL):
    """
    Setup the knowledge base using the specified model and document file.

    :param file_name: Name of the file containing the sales documents.
    :param model_name: The name of the OpenAI model to use.
    :return: RetrievalQA chain.
    """
    logger.info(f"Setting up knowledge base for {file_name}")
    vector_store = load_sales_doc_vector_store(file_name)
    logger.info("Creating RetrievalQA from vector store")
    openai_client = ChatOpenAI(api_key=Config.OPENAI_API_KEY, model=model_name)  # Use ChatOpenAI for chat models
    retriever = vector_store.as_retriever()
    return RetrievalQA.from_chain_type(
        openai_client,
        chain_type="stuff",  # Use the appropriate chain type for your use case
        retriever=retriever
    )

async def get_tools(product_catalog: str):
    """
    Initialize tools for the product catalog.

    :param product_catalog: Name of the file containing the product catalog.
    :return: List of tools.
    """
    logger.info(f"Initializing tools for product catalog {product_catalog}")
    chain = setup_knowledge_base(product_catalog, model_name=DEFAULT_MODEL)
    tools = [
        {
            "name": "ProductSearch",
            "description": "Useful for answering questions about product information.",
            "chain": chain,
        }
    ]
    logger.info("Tools setup complete")
    return tools
