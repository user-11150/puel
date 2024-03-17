class UELBaseException:
    def __init__(self, error_message):
        self.error_message = error_message
    
    def __str__(self):
        return f"{self.__class__.__name__}:{self.error_message}"