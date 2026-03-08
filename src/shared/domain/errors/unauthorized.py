class Unauthorized(Exception):
    def __init__(self, message: str = "Authentication required."):
        super().__init__(message)
