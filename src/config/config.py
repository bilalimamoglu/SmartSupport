import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file


class Config:
    """
    Configuration settings for Smart Support project.
    """
    # Determine the base directory of the project
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    PROJECT_ROOT = os.path.dirname(BASE_DIR)

    # Directory paths
    DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
    LEADS_DIR = os.path.join(DATA_DIR, 'leads')
    RESPONSES_DIR = os.path.join(DATA_DIR, 'responses')

    # Logging settings
    LOG_FILE = os.path.join(PROJECT_ROOT, 'logs', 'smart_support.log')

    # OpenAI settings
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

    # Other settings
    RESPONSE_LENGTH = 200
    LEAD_SCORE_THRESHOLD = 0.75
