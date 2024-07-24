import json
import os
from src.models.lead import Lead
from src.config.config import Config
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class LeadManager:
    """
    Manages lead data and interactions.
    """
    def __init__(self):
        self.leads = {}
        self.load_leads()

    def load_leads(self):
        """
        Load leads from the data directory.
        """
        leads_file = os.path.join(Config.LEADS_DIR, 'example_leads.json')
        if os.path.exists(leads_file):
            with open(leads_file, 'r') as file:
                leads_data = json.load(file)
                for lead_data in leads_data:
                    lead = Lead.from_dict(lead_data)
                    self.leads[lead.id] = lead
            logger.info("Leads loaded successfully.")
        else:
            logger.warning("No leads file found. Starting with an empty lead manager.")

    def save_leads(self):
        """
        Save leads to the data directory.
        """
        leads_file = os.path.join(Config.LEADS_DIR, 'leads.json')
        with open(leads_file, 'w') as file:
            json.dump([lead.to_dict() for lead in self.leads.values()], file)
        logger.info("Leads saved successfully.")

    def add_lead(self, lead):
        """
        Add a new lead.
        """
        if lead.id in self.leads:
            logger.error(f"Lead with id {lead.id} already exists.")
            return False
        self.leads[lead.id] = lead
        self.save_leads()
        logger.info(f"Lead {lead.id} added successfully.")
        return True

    def update_lead(self, lead_id, **kwargs):
        """
        Update an existing lead.
        """
        if lead_id not in self.leads:
            logger.error(f"Lead with id {lead_id} does not exist.")
            return False
        for key, value in kwargs.items():
            if hasattr(self.leads[lead_id], key):
                setattr(self.leads[lead_id], key, value)
        self.save_leads()
        logger.info(f"Lead {lead_id} updated successfully.")
        return True

    def get_lead(self, lead_id):
        """
        Retrieve a lead by ID.
        """
        return self.leads.get(lead_id)

    def get_all_leads(self):
        """
        Retrieve all leads.
        """
        return list(self.leads.values())
