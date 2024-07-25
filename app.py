# app.py

import asyncio
import chainlit as cl
from langchain_openai import OpenAI
from src.config.config import Config
from src.core.lead_manager import LeadManager
from src.core.conversation_chains import ConversationChains
from src.config.sales_stages import CONVERSATION_STAGES
from src.core.sales_assistant import SalesAssistant
from src.utils.memory import MemoryManager
from src.utils.knowledge_base import get_tools
from src.config.constants import DEFAULT_MODEL

# Initialize components
lead_manager = LeadManager()
conversation_chains = ConversationChains()
memory_manager = MemoryManager()

@cl.on_chat_start
async def on_chat_start():
    """
    Initialize the chat session and the sales assistant agent.
    """
    llm = OpenAI(api_key=Config.OPENAI_API_KEY, model=DEFAULT_MODEL)
    stage_analyzer_chain = conversation_chains.load_stage_analyzer_chain(llm)
    sales_conversation_chain = conversation_chains.load_sales_conversation_chain(llm)

    global sales_assistant
    tools = await get_tools('product_catalog.txt')

    sales_assistant = SalesAssistant(
        stage_analyzer_chain=stage_analyzer_chain,
        sales_conversation_utterance_chain=sales_conversation_chain,
        memory_manager=memory_manager,
        tools=tools,
        use_tools=True
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
    """
    Handle incoming messages from the user and generate appropriate responses from the sales assistant.

    :param message: Incoming message object from Chainlit.
    """
    user_input = message.content  # Extract the message content

    sales_assistant.human_step(user_input)

    stage_response = await sales_assistant.determine_conversation_stage()
    step_response = await sales_assistant.step()

    await cl.Message(
        content=f"*Sales Assistant thought*: {CONVERSATION_STAGES.get(stage_response, 'Unknown Stage')} \n*Current Stage*: {sales_assistant.current_stage} \n*Input*: {user_input}",
    ).send()

    await cl.Message(
        content=f"Ted Lasso: {step_response}",
    ).send()

if __name__ == "__main__":
    cl.main()
