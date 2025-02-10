from src.errors import handle_error

class ConfigKeyError(Exception):
    """Exception raised for errors in the configuration key."""
    def __init__(self, key, message="Configuration key error: '{}' not found"):
        self.key = key
        self.message = message.format(key)
        super().__init__(self.message)

# Additional imports can be added here if necessary