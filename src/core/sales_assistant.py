# src/core/sales_assistant.py

from langchain_community.llms import OpenAI
from src.config.config import Config
from src.config.sales_stages import CONVERSATION_STAGES

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
        result = await self.stage_analyzer_chain.ainvoke({
            "conversation_history": conversation_history_str
        })
        self.current_stage = result.strip()
        return self.current_stage

    async def step(self):
        conversation_history_str = "\n".join(self.conversation_history)
        result = await self.sales_conversation_utterance_chain.ainvoke({
            "salesperson_name": "Ted Lasso",
            "salesperson_role": "Business Development Representative",
            "company_name": "Sleep Haven",
            "company_business": "Sleep Haven is a premium mattress company that provides customers with the most comfortable and supportive sleeping experience possible. We offer a range of high-quality mattresses, pillows, and bedding accessories that are designed to meet the unique needs of our customers.",
            "company_values": "Our mission at Sleep Haven is to help people achieve a better night's sleep by providing them with the best possible sleep solutions. We believe that quality sleep is essential to overall health and well-being, and we are committed to helping our customers achieve optimal sleep by offering exceptional products and customer service.",
            "conversation_purpose": "find out whether they are looking to achieve better sleep via buying a premier mattress.",
            "conversation_type": "call",
            "conversation_stage": self.current_stage,
            "conversation_history": conversation_history_str,
            "tools": "",
            "tool_input": "",
            "tool_result": "",
            "agent_scratchpad": ""
        })
        response_text = result.strip()
        self.conversation_history.append(f"Ted Lasso: {response_text}")
        return response_text

    def human_step(self, human_input):
        self.conversation_history.append(f"User: {human_input}")
