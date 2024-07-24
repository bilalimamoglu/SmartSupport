from openai import AsyncOpenAI
from src.models.response import Response
from src.config.config import Config
from src.utils.logger import setup_logger
from src.utils.error_handling import ResponseGenerationError
import os
import json

logger = setup_logger(__name__)
client = AsyncOpenAI(api_key=Config.OPENAI_API_KEY)


class ResponseGenerator:
    """
    Generates sales responses using OpenAI API.
    """

    def __init__(self, responses_dir="data/responses"):
        self.responses_dir = responses_dir

    async def generate_response(self, lead, message):
        """
        Generate a response for the given lead and message.
        """
        try:
            response = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful sales assistant."},
                    {"role": "user", "content": f"Dear valued customer, {message} Best regards, Sales Team"}
                ],
                max_tokens=Config.RESPONSE_LENGTH
            )
            response_text = response.choices[0].message.content
            response_obj = Response(lead_id=lead.id, response_text=response_text)
            self.save_response(response_obj)
            logger.info(f"Response generated for lead {lead.id}")
            return response_obj
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise ResponseGenerationError from e

    def save_response(self, response):
        with open(os.path.join(self.responses_dir, f"{response.lead_id}.json"), 'w') as file:
            json.dump(response.to_dict(), file)
