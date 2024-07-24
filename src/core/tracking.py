from datetime import datetime
from src.models.response import Response
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class InteractionTracker:
    """
    Tracks interactions and updates lead status.
    """

    def __init__(self, lead_manager):
        self.lead_manager = lead_manager
        self.interactions = []

    def record_interaction(self, lead_id, interaction_type, details):
        """
        Record an interaction with a lead.
        """
        response = Response(lead_id=lead_id, response_text=details, timestamp=datetime.utcnow())
        interaction = {
            'lead_id': lead_id,
            'interaction_type': interaction_type,
            'details': response.response_text,
            'timestamp': response.timestamp.isoformat()
        }
        self.interactions.append(interaction)
        logger.info(f"Recorded {interaction_type} interaction for lead {lead_id}.")

    def get_interactions(self, lead_id):
        """
        Retrieve interactions for a specific lead.
        """
        return [interaction for interaction in self.interactions if interaction['lead_id'] == lead_id]

    def update_lead_status_based_on_interactions(self, lead_id):
        """
        Update the status of a lead based on interactions.
        """
        interactions = self.get_interactions(lead_id)
        if not interactions:
            logger.warning(f"No interactions found for lead {lead_id}.")
            return False

        # Example logic to update lead status based on interactions
        if any(interaction['interaction_type'] == 'contact' for interaction in interactions):
            self.lead_manager.update_lead(lead_id, status='contacted')
            logger.info(f"Lead {lead_id} status updated to 'contacted' based on interactions.")
        return True
