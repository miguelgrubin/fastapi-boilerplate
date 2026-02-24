class CategoryNotFound(Exception):
    def __init__(self, category_id: str):
        super().__init__(f"Category with ID {category_id} not found.")
        self.category_id = category_id
