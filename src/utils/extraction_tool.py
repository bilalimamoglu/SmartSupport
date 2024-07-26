# src/utils/extraction_tool.py

from langchain.chat_models import ChatOpenAI
from src.config.config import Config
from src.config.constants import DEFAULT_MODEL
from langchain.chains import SimpleSequentialChain
from langchain.prompts import PromptTemplate

class ExtractionTool:
    def __init__(self):
        self.llm = ChatOpenAI(api_key=Config.OPENAI_API_KEY, model_name=DEFAULT_MODEL)

    async def extract_info(self, conversation_history):
        template = """
        You are an assistant. Extract the name and contact information from the following conversation history if provided. If not provided, return "Name: Unknown, Contact: Unknown".
        Conversation History:
        {conversation_history}
        """
        prompt = PromptTemplate(input_variables=["conversation_history"], template=template)
        chain = SimpleSequentialChain(llm=self.llm, prompt=prompt)
        result = await chain.arun({"conversation_history": conversation_history})
        return result
