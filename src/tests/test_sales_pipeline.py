import unittest
from src.core.sales_pipeline import SalesPipeline
from src.core.lead_manager import LeadManager
from src.models.lead import Lead
from src.config.constants import LEAD_STATUS_NEW, LEAD_STATUS_CONTACTED

class TestSalesPipeline(unittest.TestCase):

    def setUp(self):
        self.lead_manager = LeadManager()
        self.sales_pipeline = SalesPipeline(self.lead_manager)
        lead = Lead(id="1", name="John Doe", email="john@example.com", phone="1234567890", status=LEAD_STATUS_NEW)
        self.lead_manager.add_lead(lead)

    def test_move_lead_to_next_stage(self):
        self.sales_pipeline.move_lead_to_next_stage("1")
        self.assertEqual(self.lead_manager.get_lead("1").status, LEAD_STATUS_CONTACTED)

    def test_get_leads_by_status(self):
        leads = self.sales_pipeline.get_leads_by_status(LEAD_STATUS_NEW)
        self.assertEqual(len(leads), 1)
        self.assertEqual(leads[0].name, "John Doe")

if __name__ == '__main__':
    unittest.main()
