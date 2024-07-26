# src/utils/extraction_tool.py

import logging
from langchain.chat_models import ChatOpenAI
from src.config.config import Config
from src.config.constants import DEFAULT_MODEL
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Setup logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class ExtractionTool:
    def __init__(self):
        self.llm = ChatOpenAI(api_key=Config.OPENAI_API_KEY, model_name=DEFAULT_MODEL)
        logger.info(f"Initialized ExtractionTool with model {DEFAULT_MODEL}")

    def extraction_chain(self):
        template = """
        You are an assistant. Extract the name and contact information from the following conversation history if provided. If not provided, return "Name: Unknown, Contact: Unknown".
        Conversation History:
        {conversation_history}
        """
        prompt = PromptTemplate(input_variables=["conversation_history"], template=template)
        logger.info(f"Created extraction chain with prompt: {template}")
        return LLMChain(llm=self.llm, prompt=prompt)

    async def extract_info(self, conversation_history):
        logger.info(f"Extracting info from conversation history: {conversation_history}")
        chain = self.extraction_chain()
        result = await chain.ainvoke({"conversation_history": conversation_history})
        logger.info(f"Extraction result: {result}")
        return result
