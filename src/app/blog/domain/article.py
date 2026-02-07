"""User Domain"""

from datetime import datetime

from src.app.shared.domain.domain_model import DomainModel


class Article(DomainModel):
    """Article on blog"""

    updated_at: datetime
    crated_at: datetime

    def create(self):
        """D"""

    def update(self):
        """D"""
