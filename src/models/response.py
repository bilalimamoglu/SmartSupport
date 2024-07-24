# src/models/response.py

from datetime import datetime

class Response:
    """
    Data model for a sales response.
    """
    def __init__(self, lead_id, response_text, timestamp=None):
        self.lead_id = lead_id
        self.response_text = response_text
        self.timestamp = timestamp or datetime.utcnow()

    def to_dict(self):
        """
        Convert response data to dictionary format.
        """
        return {
            'lead_id': self.lead_id,
            'response_text': self.response_text,
            'timestamp': self.timestamp.isoformat()
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create a Response instance from a dictionary.
        """
        return cls(
            lead_id=data['lead_id'],
            response_text=data['response_text'],
            timestamp=datetime.fromisoformat(data['timestamp'])
        )
