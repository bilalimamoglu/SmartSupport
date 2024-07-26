import uuid

class Lead:
    def __init__(self, id, name, contact_info, source, status):
        self.id = id
        self.name = name
        self.contact_info = contact_info
        self.source = source
        self.status = status

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            name=data["name"],
            contact_info=data["contact_info"],
            source=data["source"],
            status=data["status"]
        )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "contact_info": self.contact_info,
            "source": self.source,
            "status": self.status
        }

    def update(self, other):
        self.name = other.name
        self.contact_info = other.contact_info
        self.source = other.source
        self.status = other.status
