import asyncio
import chainlit as cl
from langchain_openai import OpenAI
from src.config.config import Config
from src.core.lead_manager import LeadManager
from src.core.response_generator import ResponseGenerator
from src.core.sales_pipeline import SalesPipeline
from src.core.tracking import InteractionTracker
from src.core.conversation_chains import ConversationChains
from src.config.sales_stages import CONVERSATION_STAGES
from src.core.sales_assistant import SalesAssistant
from src.utils.memory import MemoryManager
from src.utils.knowledge_base import setup_knowledge_base

lead_manager = LeadManager()
response_generator = ResponseGenerator()
sales_pipeline = SalesPipeline(lead_manager)
interaction_tracker = InteractionTracker(lead_manager)
conversation_chains = ConversationChains()

memory_manager = MemoryManager()
conversation_history = []

@cl.on_chat_start
async def on_chat_start():
    llm = OpenAI(api_key=Config.OPENAI_API_KEY)
    stage_analyzer_chain = conversation_chains.load_stage_analyzer_chain(llm)
    sales_conversation_chain = conversation_chains.load_sales_conversation_chain(llm)
    knowledge_base_chain = setup_knowledge_base("product_catalog.txt", llm)

    global sales_assistant
    sales_assistant = SalesAssistant(
        stage_analyzer_chain=stage_analyzer_chain,
        sales_conversation_utterance_chain=sales_conversation_chain,
        knowledge_base_chain=knowledge_base_chain,
        memory_manager=memory_manager,
        use_tools=False
    )

    sales_assistant.seed_agent()

    await cl.Message(
        content="Smart Support Sales Assistant is now running. How can I assist you today?",
    ).send()

    stages = "\n".join([f"**{stage}**: {description}" for stage, description in CONVERSATION_STAGES.items()])
    await cl.Message(
        content=f"### Conversation Stages\n{stages}",
    ).send()

@cl.on_message
async def on_message(message):
    user_input = message.content  # Extract the message content

    sales_assistant.human_step(user_input)

    if "budget" in user_input or "under" in user_input:
        kb_response = await sales_assistant.query_knowledge_base(f"Best photography equipment under {user_input}")
        await cl.Message(
            content=f"*Knowledge Base Response*: {kb_response}",
        ).send()
    else:
        stage_response = await sales_assistant.determine_conversation_stage()
        step_response = await sales_assistant.step()

        await cl.Message(
            content=f"*Sales Assistant thought*: {CONVERSATION_STAGES.get(stage_response, 'Unknown Stage')}",
        ).send()

        await cl.Message(
            content=f"Ted Lasso: {step_response}",
        ).send()

if __name__ == "__main__":
    cl.main()
