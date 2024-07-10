from .environment_models import Item, Location
import random

if __name__ == '__main__':

    # 10個のLocationインスタンスを生成
    location_list = [
        Location(
            id=i,
            items=[Item(id=i, weight=random.randint(1, 10), 
                    value=random.randint(1, 10)) for i in range(1, 6)], 
            coordinates=(random.randint(0, 1000), random.randint(0, 1000))
        ) for i in range(1, 100)
    ]

    # 既存のLocationリストに対してItemのIDを1~5に再割り当て
    for location in location_list:
        # 現在のItemリストを取得して、新しいIDを割り当てる
        new_id = 1
        for item in location.items:
            item.id = new_id
            new_id += 1

    num_locations = len(location_list)

    from .genetic_algorithm import GeneticAlgorithm
    ins = GeneticAlgorithm(5000, num_locations, 1000)
    ins.run(location_list)