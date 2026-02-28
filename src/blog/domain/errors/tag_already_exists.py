class TagAlreadyExists(Exception):
    def __init__(self, message: str):
        super().__init__("Tag already exists. " + message)
