from typing import List

from dataclasses import dataclass


@dataclass(frozen=True)
class AuthenticatedUser:
    sub: str
    username: str
    email: str
    groups: List[str]
    name: str
