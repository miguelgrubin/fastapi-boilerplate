class TagNotFound(Exception):
    def __init__(self, tag_id: str):
        super().__init__(f"Tag with ID {tag_id} not found.")
        self.tag_id = tag_id
