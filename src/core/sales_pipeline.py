from src.models.lead import Lead
from src.config.constants import (
    LEAD_STATUS_NEW,
    LEAD_STATUS_CONTACTED,
    LEAD_STATUS_QUALIFIED,
    LEAD_STATUS_CONVERTED,
    LEAD_STATUS_UNQUALIFIED
)
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class SalesPipeline:
    """
    Manages the sales pipeline.
    """

    def __init__(self, lead_manager):
        self.lead_manager = lead_manager

    def move_lead_to_next_stage(self, lead_id):
        """
        Move the lead to the next stage in the sales pipeline.
        """
        lead = self.lead_manager.get_lead(lead_id)
        if not lead:
            logger.error(f"Lead {lead_id} not found.")
            return False

        if lead.status == LEAD_STATUS_NEW:
            lead.update_status(LEAD_STATUS_CONTACTED)
        elif lead.status == LEAD_STATUS_CONTACTED:
            lead.update_status(LEAD_STATUS_QUALIFIED)
        elif lead.status == LEAD_STATUS_QUALIFIED:
            lead.update_status(LEAD_STATUS_CONVERTED)
        else:
            lead.update_status(LEAD_STATUS_UNQUALIFIED)

        self.lead_manager.update_lead(lead.id, status=lead.status)
        logger.info(f"Lead {lead.id} moved to {lead.status}.")
        return True

    def get_leads_by_status(self, status):
        """
        Retrieve leads by status.
        """
        return [lead for lead in self.lead_manager.get_all_leads() if lead.status == status]