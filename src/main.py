# src/main.py

import sys
import os
import asyncio

# Add the src directory to the sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from langchain_openai import OpenAI
from src.config.config import Config
from src.core.lead_manager import LeadManager
from src.core.response_generator import ResponseGenerator
from src.core.sales_pipeline import SalesPipeline
from src.core.tracking import InteractionTracker
from src.core.conversation_chains import ConversationChains
from src.config.sales_stages import CONVERSATION_STAGES
from src.core.sales_assistant import SalesAssistant  # Import the SalesAssistant class

# Initialize components
lead_manager = LeadManager()
response_generator = ResponseGenerator()
sales_pipeline = SalesPipeline(lead_manager)
interaction_tracker = InteractionTracker(lead_manager)
conversation_chains = ConversationChains()

async def main():
    llm = OpenAI(api_key=Config.OPENAI_API_KEY)
    stage_analyzer_chain = conversation_chains.load_stage_analyzer_chain(llm)
    sales_conversation_chain = conversation_chains.load_sales_conversation_chain(llm)

    sales_assistant = SalesAssistant(
        stage_analyzer_chain=stage_analyzer_chain,
        sales_conversation_utterance_chain=sales_conversation_chain,
        use_tools=False
    )

    sales_assistant.seed_agent()

    stage_response = await sales_assistant.determine_conversation_stage()
    print(f"Conversation Stage: {CONVERSATION_STAGES[stage_response]}")

    step_response = await sales_assistant.step()
    print(f"Sales Assistant Response: {step_response}")

if __name__ == "__main__":
    asyncio.run(main())
