from dataclasses import dataclass

from src.blog.domain.article_repository import ArticleRepository
from src.blog.domain.category_repository import CategoryRepository
from src.blog.domain.comment_repository import CommentRepository
from src.blog.domain.tag_repository import TagRepository
from src.blog.domain.user_repository import UserRepository
from src.blog.use_cases.article_creator import ArticleCreator
from src.blog.use_cases.article_deleter import ArticleDeleter
from src.blog.use_cases.article_finder import ArticleFinder
from src.blog.use_cases.article_lister import ArticleLister
from src.blog.use_cases.article_publisher import ArticlePublisher
from src.blog.use_cases.article_updater import ArticleUpdater
from src.blog.use_cases.category_creator import CategoryCreator
from src.blog.use_cases.category_lister import CategoryLister
from src.blog.use_cases.comment_creator import CommentCreator
from src.blog.use_cases.comment_deleter import CommentDeleter
from src.blog.use_cases.comment_lister import CommentLister
from src.blog.use_cases.tag_creator import TagCreator
from src.blog.use_cases.tag_lister import TagLister
from src.blog.use_cases.user_creator import UserCreator
from src.blog.use_cases.user_deleter import UserDeleter


@dataclass
class BlogRepositoriesType:
    user_repository: UserRepository
    article_repository: ArticleRepository
    comment_repository: CommentRepository
    category_repository: CategoryRepository
    tag_repository: TagRepository


@dataclass
class BlogUseCasesType:
    user_creator: UserCreator
    user_deleter: UserDeleter
    article_creator: ArticleCreator
    article_finder: ArticleFinder
    article_lister: ArticleLister
    article_updater: ArticleUpdater
    article_deleter: ArticleDeleter
    article_publisher: ArticlePublisher
    comment_creator: CommentCreator
    comment_lister: CommentLister
    comment_deleter: CommentDeleter
    category_creator: CategoryCreator
    category_lister: CategoryLister
    tag_creator: TagCreator
    tag_lister: TagLister
