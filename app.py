# app.py

import streamlit as st
import asyncio
import os
import json
from openai import AsyncOpenAI
from langchain_community.llms import OpenAI
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

async def run_sales_assistant():
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
    st.write(f"Conversation Stage: {CONVERSATION_STAGES[stage_response]}")

    step_response = await sales_assistant.step()
    st.write(f"Sales Assistant Response: {step_response}")

# Set up Streamlit UI
st.title("Smart Support Sales Assistant")

# Sidebar for database and other information
with st.sidebar:
    st.header("Database and Info")
    show_leads = st.checkbox("Show All Leads")
    show_responses = st.checkbox("Show All Responses")

    if show_leads:
        st.subheader("All Leads")
        all_leads = lead_manager.get_all_leads()
        for lead in all_leads:
            st.json(lead.to_dict())

    if show_responses:
        st.subheader("All Responses")
        response_files = os.listdir(Config.RESPONSES_DIR)
        for response_file in response_files:
            with open(os.path.join(Config.RESPONSES_DIR, response_file), 'r') as f:
                response_data = json.load(f)
                st.json(response_data)

# Input box for user query
user_input = st.text_input("Enter your query:")

if st.button("Get Response"):
    lead_id = "1"  # For demonstration purposes, using lead ID 1
    lead = lead_manager.get_lead(lead_id)

    if lead and user_input:
        # Generate response
        response = asyncio.run(response_generator.generate_response(lead, user_input))
        st.write(f"Response: {response.response_text}")

        # Record interaction
        interaction_tracker.record_interaction(lead.id, "email", response.response_text)

        # Move lead to the next stage in the sales pipeline
        sales_pipeline.move_lead_to_next_stage(lead.id)

        # Display lead details
        st.subheader("Lead Information")
        st.json(lead.to_dict())

        # Display interaction history
        st.subheader("Interaction History")
        interactions = interaction_tracker.get_interactions(lead.id)
        for interaction in interactions:
            st.write(f"{interaction['timestamp']}: {interaction['details']}")

        # Display sales pipeline stage
        st.subheader("Sales Pipeline Stage")
        st.write(f"Current Stage: {lead.status}")

# Initialize and run the Sales Assistant
if st.button("Run Sales Assistant"):
    asyncio.run(run_sales_assistant())
