import uuid

class Lead:
    def __init__(self, name, contact_info, source, status="new", lead_id=None):
        self.id = lead_id or str(uuid.uuid4())
        self.name = name
        self.contact_info = contact_info
        self.source = source
        self.status = status

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data.get("name", "Unknown"),
            contact_info=data.get("contact_info", "Unknown"),
            source=data.get("source", "Unknown"),
            status=data.get("status", "new"),
            lead_id=data.get("id")  # Handle missing 'id' key
        )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "contact_info": self.contact_info,
            "source": self.source,
            "status": self.status
        }
