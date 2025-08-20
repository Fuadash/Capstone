from dataclasses import dataclass
from typing import Tuple, List


@dataclass
class Filters:
    year_range: Tuple[int, int]
    price_range: Tuple[float, float]
    tags: List[str]
    platform: str  # "All" | "Windows" | "Mac" | "Linux"
    nsfw: str  # "Yes" | "No"
