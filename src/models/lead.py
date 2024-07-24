class Lead:
    def __init__(self, id, name, email, phone, status='new'):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.status = status

    @classmethod
    def from_dict(cls, data):
        return cls(data['id'], data['name'], data['email'], data['phone'], data.get('status', 'new'))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'status': self.status
        }

    def update_status(self, new_status):
        self.status = new_status
