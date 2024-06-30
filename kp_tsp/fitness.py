import math

from .environment_models import Location

def _calculate_distance(p1, p2):
    """
    ユークリッド距離を計算するヘルパー関数
    """
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

def calculate_fitness(gene: list[tuple[int, int]], locations: list[Location], max_weight: int) -> float:
    """
    適応度計算
    (将来クラス化してLocationとmax weightを固定したい)

    Parameters
    ----------
    gene : list[tuple[int, int]]
        遺伝子
    locations : list[Location]
        各拠点とそのアイテム、座標のリスト
    max_weight : int
        ナップザックの制限重量

     Returns
    -------
    適応度 : float
        適応度スコア
    """
    total_value = 0
    total_weight = 0
    total_distance = 0
    current_position = (0, 0)  # 初期位置を(0,0)とする

    # 遺伝子に含まれる各タプルを解析して価値と距離を計算
    for loc_id, item_id in gene:
        location = next(loc for loc in locations if loc.id == loc_id)
        item = next(item for item in location.items if item.id == item_id)

        # アイテムの重さと価値を加算
        if total_weight + item.weight <= max_weight:
            total_weight += item.weight
            total_value += item.value

            # 拠点間の移動距離を加算
            total_distance += _calculate_distance(current_position, location.coordinates)
            current_position = location.coordinates
        else:
            # 重量オーバーの場合、ペナルティとして適応度を下げる
            return 0

    # 適応度の計算。価値を最大化し、距離を最小化したいので、価値を距離で割る
    if total_distance > 0:
        return total_value / total_distance
    return 0