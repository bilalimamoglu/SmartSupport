import sys
import os
import asyncio

# Add the parent directory of src to the sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config.config import Config
from src.core.lead_manager import LeadManager
from src.core.response_generator import ResponseGenerator
from src.core.sales_pipeline import SalesPipeline
from src.core.tracking import InteractionTracker
from src.utils.logger import setup_logger
from src.models.lead import Lead  # Import Lead model

logger = setup_logger(__name__)


async def main():
    logger.info("Starting Smart Support application.")

    # Ensure necessary directories exist
    logger.info("Checking and creating necessary directories if not present.")
    os.makedirs(Config.LEADS_DIR, exist_ok=True)
    os.makedirs(Config.RESPONSES_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(Config.LOG_FILE), exist_ok=True)

    # Initialize components
    logger.info("Initializing lead manager, response generator, sales pipeline, and interaction tracker.")
    lead_manager = LeadManager()
    response_generator = ResponseGenerator()
    sales_pipeline = SalesPipeline(lead_manager)
    interaction_tracker = InteractionTracker(lead_manager)

    # Load some example leads (if not already present)
    logger.info("Checking if example leads need to be loaded.")
    if not os.listdir(Config.LEADS_DIR):
        logger.info("No leads found in directory. Loading example leads.")
        example_leads = [
            {"id": "1", "name": "John Doe", "email": "john@example.com", "phone": "1234567890"},
            {"id": "2", "name": "Jane Smith", "email": "jane@example.com", "phone": "0987654321"}
        ]
        for lead_data in example_leads:
            lead = Lead.from_dict(lead_data)
            lead_manager.add_lead(lead)
        logger.info("Example leads added.")

    # Simulate generating a response for a lead
    logger.info("Attempting to generate a response for lead ID 1.")
    lead = lead_manager.get_lead("1")
    if lead:
        message = "We are excited to offer you our new product."
        response = await response_generator.generate_response(lead, message)
        logger.info(f"Generated response: {response.response_text}")

        # Record interaction
        logger.info(f"Recording interaction for lead ID {lead.id}.")
        interaction_tracker.record_interaction(lead.id, "email", response.response_text)

    # Simulate moving the lead to the next stage in the pipeline
    logger.info(f"Moving lead ID {lead.id} to the next stage in the sales pipeline.")
    sales_pipeline.move_lead_to_next_stage("1")


if __name__ == "__main__":
    logger.info("Running main function.")
    asyncio.run(main())
