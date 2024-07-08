import random
import math

from kp_tsp.environment_models import Location

gene_type = list[tuple[bool, int, int]]

class Individual:
    """
    遺伝子の情報と適応度計算、突然変異の関数を保持する

    Attributes
    ----------
    gene : gene_type
       遺伝子本体
    fitness : float
        この遺伝子の適応度
    """

    def __init__(self, num_place: int = -1) -> None:
        """
        遺伝子のインスタンス化。
        num_placeが入力されない場合は、インスタンス化したのちにgeneを後から入れることを想定する。

        Parameters
        ----------
        num_place : int
            拠点数
        """
        if num_place == -1:
            self.gene: gene_type = []
        else:
            self.gene = self.initialize_gene(num_place)

        self.fitness: float = 0
        self.total_dist: float = 0
        self.total_value: int = 0
        self.total_weight: int = 0

        self.normalized_dist: float = 0
        self.normalized_value: float = 0
        self.normalized_weight: float = 0
        
    def initialize_gene(self, num_place: int) -> gene_type:
        """
        遺伝子の初期化

        Parameters
        ----------
        num_place : int
            拠点数

        Returns
        -------
        遺伝子 : gene_type
            初期化された遺伝子
        """
        # 1からnum_placeまでの範囲で重複のないランダムな数字を生成
        visit = random.sample(range(1, num_place + 1), num_place)

        # 1から5までのランダムな数字を生成
        item = [random.randint(1, 5) for _ in range(num_place)]

        is_visited = [random.choice([True, False]) for _ in range(num_place)]

        return list(zip(is_visited, visit, item))
    
    def _calculate_distance(self, p1: tuple[int, int], p2: tuple[int, int]) -> float:
        """
        ユークリッド距離を計算するヘルパー関数
        """
        return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
    
    def calc_total(self, locations: list[Location]):
        """
        各種のTotal計算
        fitness計算はpopulationに委譲

        Parameters
        ----------
        location : list[Locations]
            拠点数
        """

        total_value = 0
        total_weight = 0
        total_distance = 0.0
        current_position = (0, 0)  # 初期位置を(0,0)とする

        # 遺伝子に含まれる各タプルを解析して価値と距離を計算
        for is_visited, loc_id, item_id in self.gene:
            location = next(loc for loc in locations if loc.id == loc_id)
            item = next(item for item in location.items if item.id == item_id)

            if is_visited:
                # アイテムの重さと価値を加算
                total_weight += item.weight
                total_value += item.value

                # 拠点間の移動距離を加算
                total_distance += self._calculate_distance(current_position, location.coordinates)
                current_position = location.coordinates

        # 適応度の計算。価値を最大化し、距離を最小化したいので、価値を距離で割る
        if total_distance > 0 and total_value > 0:
            self.total_dist = total_distance
            self.total_value = total_value
            self.total_weight = total_weight

    def mutate(self, mutation_rate: float):
        """
        遺伝子の突然変異を行う

        Parameters
        ----------
        gene : gene_type
            現在の遺伝子
        locations : list[Location]
            拠点とアイテムのリスト
        mutation_rate: float
            各要素に対する変異の確率
        """
        new_gene = self.gene.copy()
        for i in range(len(self.gene)):
            if random.random() <= mutation_rate:
                is_visited = random.choice([True, False])
                visit = self.gene[i][1]
                item = random.randint(1, 5)
                new_gene[i] = (is_visited, visit, item)
        self.gene = new_gene
