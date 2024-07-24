class LeadDataError(Exception):
    """
    Exception raised for errors in the lead data.
    """
    def __init__(self, message="Invalid lead data provided."):
        self.message = message
        super().__init__(self.message)

class ResponseGenerationError(Exception):
    """
    Exception raised for errors in generating a response.
    """
    def __init__(self, message="Failed to generate response."):
        self.message = message
        super().__init__(self.message)
