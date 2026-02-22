class ArticleNotFound(Exception):
    def __init__(self, article_id: str):
        super().__init__(f"Article with ID {article_id} not found.")
        self.article_id = article_id
