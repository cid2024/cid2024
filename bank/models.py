from dataclasses import dataclass
from typing import Literal


@dataclass(kw_only=True)
class StatementElement:
    type: Literal["text", "image", "embed_image"]
    data: str


@dataclass(kw_only=True)
class Problem:
    id: str
    statement: list[StatementElement]
    choice: list[tuple[str, list[StatementElement]]]
    answer: str
    explanation: str
