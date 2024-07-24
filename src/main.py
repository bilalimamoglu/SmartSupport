import sys
import os
import asyncio

# Add the src directory to the sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from openai import AsyncOpenAI
from src.config.config import Config
from src.core.lead_manager import LeadManager
from src.core.response_generator import ResponseGenerator
from src.core.sales_pipeline import SalesPipeline
from src.core.tracking import InteractionTracker
from src.core.conversation_chains import ConversationChains
from src.config.sales_stages import CONVERSATION_STAGES

# Initialize components
lead_manager = LeadManager()
response_generator = ResponseGenerator()
sales_pipeline = SalesPipeline(lead_manager)
interaction_tracker = InteractionTracker(lead_manager)
conversation_chains = ConversationChains()


class SalesAssistant:
    def __init__(self, stage_analyzer_chain, sales_conversation_utterance_chain, use_tools=False):
        self.stage_analyzer_chain = stage_analyzer_chain
        self.sales_conversation_utterance_chain = sales_conversation_utterance_chain
        self.use_tools = use_tools
        self.conversation_history = []
        self.current_stage = "1"

    def seed_agent(self):
        self.conversation_history = []
        self.current_stage = "1"

    async def determine_conversation_stage(self):
        conversation_history_str = "\n".join(self.conversation_history)
        result = await self.stage_analyzer_chain.call({
            "conversation_history": conversation_history_str
        })
        self.current_stage = result['text']
        return self.current_stage

    async def step(self):
        conversation_history_str = "\n".join(self.conversation_history)
        result = await self.sales_conversation_utterance_chain.call({
            "salesperson_name": "Ted Lasso",
            "salesperson_role": "Business Development Representative",
            "company_name": "Sleep Haven",
            "company_business": "Sleep Haven is a premium mattress company that provides customers with the most comfortable and supportive sleeping experience possible. We offer a range of high-quality mattresses, pillows, and bedding accessories that are designed to meet the unique needs of our customers.",
            "company_values": "Our mission at Sleep Haven is to help people achieve a better night's sleep by providing them with the best possible sleep solutions. We believe that quality sleep is essential to overall health and well-being, and we are committed to helping our customers achieve optimal sleep by offering exceptional products and customer service.",
            "conversation_purpose": "find out whether they are looking to achieve better sleep via buying a premier mattress.",
            "conversation_type": "call",
            "conversation_stage": self.current_stage,
            "conversation_history": conversation_history_str
        })
        response_text = result['text']
        self.conversation_history.append(f"Ted Lasso: {response_text}")
        return response_text

    def human_step(self, human_input):
        self.conversation_history.append(f"User: {human_input}")


async def main():
    llm = AsyncOpenAI(api_key=Config.OPENAI_API_KEY)
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
