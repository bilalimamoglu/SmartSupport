import uuid

class Lead:
    def __init__(self, name, contact_info, source, status, lead_id=None):
        self.id = lead_id if lead_id else str(uuid.uuid4())
        self.name = name
        self.contact_info = contact_info
        self.source = source
        self.status = status

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "contact_info": self.contact_info,
            "source": self.source,
            "status": self.status
        }

    @staticmethod
    def from_dict(data):
        return Lead(
            lead_id=data.get("id"),
            name=data.get("name"),
            contact_info=data.get("contact_info"),
            source=data.get("source"),
            status=data.get("status")
        )
