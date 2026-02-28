"""Slug Value Object"""

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Slug:
    """Value object representing a URL-friendly slug.

    Rules:
    - Lowercase letters a-z and hyphens only
    - Generated from a name/title by lowercasing, replacing spaces and
      non-allowed characters with hyphens, collapsing consecutive hyphens,
      and stripping leading/trailing hyphens.
    """

    value: str

    @classmethod
    def from_name(cls, name: str) -> "Slug":
        """Create a Slug from a human-readable name or title.

        Example:
            Slug.from_name("My fav post") -> Slug(value="my-fav-post")
        """
        slug = name.lower()
        slug = re.sub(r"[^a-z\-\s]", "", slug)
        slug = re.sub(r"[\s\-]+", "-", slug)
        slug = slug.strip("-")
        return cls(value=slug)
