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

# # 100個のItemインスタンスを生成
# item_list = [Item(id=i, weight=random.randint(1, 10), 
#               value=random.randint(1, 10)) for i in range(1, 101)]

# # 100個のLocationインスタンスを生成
# location_list = [
#     Location(
#         id=i,
#         items=random.sample(item_list, 5),  # Itemリストからランダムに5つ選択
#         coordinates=(random.randint(0, 1000), random.randint(0, 1000))
#     ) for i in range(1, 101)
# ]