# src/config/config.py

import os

class Config:
    """
    Configuration settings for Sales GPT project.
    """
    # Directory paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    LEADS_DIR = os.path.join(DATA_DIR, 'leads')
    RESPONSES_DIR = os.path.join(DATA_DIR, 'responses')

    # Logging settings
    LOG_FILE = os.path.join(BASE_DIR, 'logs', 'sales_gpt.log')

    # LangChain settings
    LANGCHAIN_API_KEY = os.getenv('LANGCHAIN_API_KEY', 'your-langchain-api-key')

    # Other settings
    RESPONSE_LENGTH = 200
    LEAD_SCORE_THRESHOLD = 0.75
