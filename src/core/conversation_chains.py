# src/core/conversation_chains.py

from langchain_openai import OpenAI
from src.config.config import Config
from src.config.sales_stages import SALES_PROMPT_TEMPLATE, CONVERSATION_STAGES
from langchain.prompts import PromptTemplate

class ConversationChains:
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)

    def load_stage_analyzer_chain(self, llm, verbose: bool = False):
        prompt = PromptTemplate(
            template="""
            You are a sales assistant helping your sales agent determine which stage of a sales conversation to stay at or move to when talking to a user.
            Below is the conversation history. Use it to make your decision.
            Only use the text between the first and second '===' to complete the task.
            ===
            {conversation_history}
            ===
            Now determine the next immediate conversation stage for the agent in the sales conversation by selecting only from the following options:
            1. Introduction: Start the conversation by introducing yourself and your company. Be polite and respectful while keeping the tone of the conversation professional.
            2. Qualification: Ensure the prospect is the right person to talk to regarding your product/service and has the authority to make purchasing decisions.
            3. Value proposition: Explain briefly how your product/service can benefit the prospect, focusing on unique selling points.
            4. Needs analysis: Ask open-ended questions to uncover the prospect's needs and pain points. Listen attentively to their responses.
            5. Solution presentation: Present your product/service as the solution to the prospect's needs, based on the information gathered.
            6. Objection handling: Address any objections the prospect may have regarding your product/service with evidence or testimonials.
            7. Close: Propose the next step, such as a demo, trial, or meeting. Summarize the discussion and reiterate the benefits.
            8. End conversation: End the call if there is nothing else to discuss.

            Only answer with a number between 1 and 8 based on the best guess of what stage the conversation should continue with.
            If there is no conversation history, output 1.
            The answer should be a single number only, no words.
            """,
            input_variables=["conversation_history"]
        )
        return prompt, llm

    def load_sales_conversation_chain(self, llm, verbose: bool = False):
        prompt = PromptTemplate(
            template=SALES_PROMPT_TEMPLATE,
            input_variables=[
                "salesperson_name", "salesperson_role", "company_name",
                "company_business", "company_values", "conversation_purpose",
                "conversation_type", "conversation_stage", "conversation_history",
                "tools"  # Include tools as a placeholder
            ]
        )
        return prompt, llm
