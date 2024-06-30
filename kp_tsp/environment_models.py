from dataclasses import dataclass
import random

@dataclass
class Item:
    id: int
    weight: int
    value: int

@dataclass
class Location:
    id: int
    items: list[Item]
    coordinates: tuple[int, int]