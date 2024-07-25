import re
from src.utils.memory import MemoryManager
from src.utils.knowledge_base import setup_knowledge_base, get_tools

class SalesAssistant:
    def __init__(self, stage_analyzer_chain, sales_conversation_utterance_chain, memory_manager, tools=None, use_tools=False):
        self.stage_analyzer_chain = stage_analyzer_chain
        self.sales_conversation_utterance_chain = sales_conversation_utterance_chain
        self.memory_manager = memory_manager
        self.tools = tools if tools else []
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

        stage_number = re.search(r'\d+', result)
        if stage_number:
            self.current_stage = stage_number.group().strip()
        else:
            self.current_stage = "Unknown"

        return self.current_stage

    async def step(self):
        conversation_history_str = "\n".join(self.conversation_history)
        if self.use_tools:
            tool_response = await self.tools[0]['chain'].acall({
                "query": conversation_history_str
            })
            response_text = tool_response['result']
        else:
            result = await self.sales_conversation_utterance_chain.ainvoke({
                "salesperson_name": "Ted Lasso",
                "salesperson_role": "Business Development Representative",
                "company_name": "Photo Gear Pro",
                "company_business": "Photo Gear Pro is a leading retailer of high-quality photography equipment, offering cameras, lenses, tripods, lighting, and accessories to help photographers capture the perfect shot.",
                "company_values": "At Photo Gear Pro, we are committed to providing photographers with the best tools and advice to help them achieve their creative vision. We believe in the power of photography to tell stories, capture memories, and inspire others.",
                "conversation_purpose": "understand your photography needs and recommend the best equipment to enhance your photography skills.",
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

        self.memory_manager.save_to_memory(self.conversation_history)

        return response_text

    def human_step(self, human_input):
        self.conversation_history.append(f"User: {human_input}")
        self.memory_manager.update_short_term_memory(human_input)
