class Lead:
    """
    Data model for a sales lead.
    """
    def __init__(self, id, name, email, phone, status='new', score=0.0):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.status = status
        self.score = score

    def update_status(self, new_status):
        """
        Update the status of the lead.
        """
        self.status = new_status

    def update_score(self, new_score):
        """
        Update the score of the lead.
        """
        self.score = new_score

    def to_dict(self):
        """
        Convert lead data to dictionary format.
        """
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'status': self.status,
            'score': self.score
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create a Lead instance from a dictionary.
        """
        return cls(
            id=data['id'],
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            status=data.get('status', 'new'),
            score=data.get('score', 0.0)
        )
