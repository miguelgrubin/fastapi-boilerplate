from typing import Dict, List, Tuple

from src.blog.domain.article import Article
from src.blog.domain.article_repository import ArticleRepository
from src.shared.use_cases.use_case import UseCase


class ArticleLister(UseCase):
    def __init__(self, article_repository: ArticleRepository) -> None:
        self.article_repository = article_repository

    def execute(
        self,
        find_filters: Dict = {},
        find_order: Dict = {},
        find_limits: Tuple[int, int] = (0, 20),
    ) -> List[Article]:
        return self.article_repository.find_all(find_filters, find_order, find_limits)
