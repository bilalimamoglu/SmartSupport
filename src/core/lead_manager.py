from src.models.lead import Lead
import json
import os

class LeadManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.leads = self.load_leads()

    def load_leads(self):
        leads_data = self.db_manager.get_all_leads()
        return [Lead.from_dict(ld) for ld in leads_data]

    def add_or_update_lead(self, lead):
        existing_lead = self.get_lead_by_id(lead.id)
        if existing_lead:
            existing_lead.update(lead)
        else:
            self.leads.append(lead)
        self.db_manager.add_or_update_lead(lead)

    def get_lead_by_id(self, lead_id):
        for lead in self.leads:
            if lead.id == lead_id:
                return lead
        return None
