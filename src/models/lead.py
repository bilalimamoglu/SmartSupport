# src/models/lead.py

class Lead:
    def __init__(self, id, name, email, phone, status='new'):
        """
        Initialize a Lead object.

        :param id: The unique ID of the lead.
        :param name: The name of the lead.
        :param email: The email address of the lead.
        :param phone: The phone number of the lead.
        :param status: The status of the lead, defaults to 'new'.
        """
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.status = status

    @classmethod
    def from_dict(cls, data):
        """
        Create a Lead instance from a dictionary.

        :param data: A dictionary containing lead information.
        :return: A Lead instance.
        """
        return cls(data['id'], data['name'], data['email'], data['phone'], data.get('status', 'new'))

    def to_dict(self):
        """
        Convert the lead object to a dictionary.

        :return: A dictionary representation of the lead.
        """
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'status': self.status
        }

    def update_status(self, new_status):
        """
        Update the status of the lead.

        :param new_status: The new status to set.
        """
        self.status = new_status