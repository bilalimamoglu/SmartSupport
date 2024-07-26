import json
import os
from src.models.lead import Lead

class LeadManager:
    def __init__(self, leads_file='data/leads/example_leads.json'):
        self.leads_file = leads_file
        self.leads = self.load_leads()

    def load_leads(self):
        if not os.path.exists(self.leads_file):
            return []
        with open(self.leads_file, 'r') as file:
            leads_data = json.load(file)
        return [Lead.from_dict(ld) for ld in leads_data]

    def save_leads(self):
        with open(self.leads_file, 'w') as file:
            json.dump([lead.to_dict() for lead in self.leads], file)

    def add_lead(self, lead):
        self.leads.append(lead)
        self.save_leads()
