import unittest
from datetime import datetime
from src.core.tracking import InteractionTracker
from src.core.lead_manager import LeadManager
from src.models.lead import Lead

class TestInteractionTracker(unittest.TestCase):

    def setUp(self):
        self.lead_manager = LeadManager()
        self.tracker = InteractionTracker(self.lead_manager)
        lead = Lead(id="1", name="John Doe", email="john@example.com", phone="1234567890")
        self.lead_manager.add_lead(lead)

    def test_record_interaction(self):
        self.tracker.record_interaction("1", "email", "Sent a welcome email.")
        interactions = self.tracker.get_interactions("1")
        self.assertEqual(len(interactions), 1)
        self.assertEqual(interactions[0]['details'], "Sent a welcome email.")

    def test_update_lead_status_based_on_interactions(self):
        self.tracker.record_interaction("1", "contact", "Called the lead.")
        self.tracker.update_lead_status_based_on_interactions("1")
        self.assertEqual(self.lead_manager.get_lead("1").status, "contacted")

if __name__ == '__main__':
    unittest.main()
