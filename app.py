import streamlit as st
import asyncio
import os
import json
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
        self.current_stage = result['text'].strip()
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

# Function to initialize and run the Sales Assistant
async def run_sales_assistant():
    llm = AsyncOpenAI(api_key=Config.OPENAI_API_KEY)
    stage_analyzer_chain = conversation_chains.load_stage_analyzer_chain(llm)
    sales_conversation_chain = conversation_chains.load_sales_conversation_chain(llm)

    sales_assistant = SalesAssistant(
        stage_analyzer_chain=stage_analyzer_chain,
        sales_conversation_utterance_chain=sales_conversation_chain,
        use_tools=False
    )

    sales_assistant.seed_agent()

    while True:
        stage_response = await sales_assistant.determine_conversation_stage()
        st.write(f"Conversation Stage: {CONVERSATION_STAGES[stage_response]}")

        if st.button("Continue Conversation"):
            user_input = st.text_input("Enter your message:")
            sales_assistant.human_step(user_input)
            step_response = await sales_assistant.step()
            st.write(f"Sales Assistant Response: {step_response}")
            st.session_state.conversation_history = sales_assistant.conversation_history

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
