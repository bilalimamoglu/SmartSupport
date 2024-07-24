import unittest
from src.models.lead import Lead
from src.core.lead_manager import LeadManager

class TestLeadManager(unittest.TestCase):

    def setUp(self):
        self.lead_manager = LeadManager()

    def test_add_lead(self):
        lead = Lead(id="1", name="John Doe", email="john@example.com", phone="1234567890")
        result = self.lead_manager.add_lead(lead)
        self.assertTrue(result)
        self.assertEqual(self.lead_manager.get_lead("1").name, "John Doe")

    def test_update_lead(self):
        lead = Lead(id="2", name="Jane Doe", email="jane@example.com", phone="0987654321")
        self.lead_manager.add_lead(lead)
        self.lead_manager.update_lead("2", name="Jane Smith")
        self.assertEqual(self.lead_manager.get_lead("2").name, "Jane Smith")

    def test_get_lead(self):
        lead = Lead(id="3", name="Alice", email="alice@example.com", phone="1111111111")
        self.lead_manager.add_lead(lead)
        self.assertIsNotNone(self.lead_manager.get_lead("3"))

    def test_get_all_leads(self):
        lead1 = Lead(id="4", name="Bob", email="bob@example.com", phone="2222222222")
        lead2 = Lead(id="5", name="Charlie", email="charlie@example.com", phone="3333333333")
        self.lead_manager.add_lead(lead1)
        self.lead_manager.add_lead(lead2)
        self.assertEqual(len(self.lead_manager.get_all_leads()), 2)

if __name__ == '__main__':
    unittest.main()
