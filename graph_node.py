from dataclasses import dataclass
from typing import List


@dataclass()
class GraphNode:
    name: str
    version: str
    dependencies: List = None
    def __post_init__(self):
        self.dependencies = []