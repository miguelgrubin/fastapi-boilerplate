class CommentNotFound(Exception):
    def __init__(self, comment_id: str):
        super().__init__(f"Comment with ID {comment_id} not found.")
        self.comment_id = comment_id
