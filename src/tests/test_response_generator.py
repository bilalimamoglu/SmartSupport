import unittest
from unittest.mock import patch
from src.core.response_generator import ResponseGenerator
from src.models.lead import Lead

class TestResponseGenerator(unittest.TestCase):

    @patch('src.core.response_generator.openai.Completion.create')
    def setUp(self, MockOpenAI):
        self.mock_openai = MockOpenAI
        self.mock_openai.return_value.choices = [type('', (), {"text": "Generated response"})()]
        self.response_generator = ResponseGenerator()

    def test_generate_response(self):
        lead = Lead(id="1", name="John Doe", email="john@example.com", phone="1234567890")
        response = self.response_generator.generate_response(lead, "Hello")
        self.assertEqual(response.response_text, "Generated response")
        self.assertEqual(response.lead_id, "1")

if __name__ == '__main__':
    unittest.main()
