import json
import os
from src.config.config import Config
from src.models.lead import Lead

class LeadManager:
    def __init__(self, leads_dir="data/leads"):
        self.leads_dir = leads_dir
        self.leads = {}
        self.load_leads()

    def load_leads(self):
        if os.path.exists(self.leads_dir):
            for filename in os.listdir(self.leads_dir):
                if filename.endswith(".json"):
                    with open(os.path.join(self.leads_dir, filename), 'r') as f:
                        lead_data = json.load(f)
                        if isinstance(lead_data, list):
                            for lead_dict in lead_data:
                                lead = Lead.from_dict(lead_dict)
                                self.leads[lead.id] = lead
                        else:
                            lead = Lead.from_dict(lead_data)
                            self.leads[lead.id] = lead

    def save_leads(self):
        for lead in self.leads.values():
            with open(os.path.join(self.leads_dir, f"{lead.id}.json"), 'w') as f:
                json.dump(lead.to_dict(), f)

    def get_lead(self, lead_id):
        return self.leads.get(lead_id)

    def add_lead(self, lead):
        self.leads[lead.id] = lead
        self.save_leads()

    def get_all_leads(self):
        return list(self.leads.values())
