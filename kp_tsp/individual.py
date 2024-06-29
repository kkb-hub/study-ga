import random

from .fitness import calculate_fitness

gene_type = list[tuple[int, int]]

class Individual:

    def __init__(self, max_place: int | None = None) -> None:
        """
        染色体クラスの初期化
        : praram max_place: 拠点数
        """
        if max_place == None:
            self.gene: gene_type = []
        else:
            self.gene = self.initialize_gene(max_place)
        self.fitness: float = 0
        
    def initialize_gene(self, max_place) -> gene_type:
        """
        遺伝子の初期化
        遺伝子のサイズは拠点数の1/4から1/2の範囲でランダムに選ばれる。
        : return : 初期化された遺伝子
        """
        gene_size = random.randint(max_place // 4, max_place // 2)

        # 1からmax_placeまでの範囲で重複のないランダムな数字を生成
        visit = random.sample(range(1, max_place + 1), gene_size)

        # 1から5までのランダムな数字を生成
        item = [random.randint(1, 5) for _ in range(gene_size)]

        return list(zip(visit, item))
    
    def evaluate_fitness(self, locations, max_weight):
        self.fitness = calculate_fitness(self.gene, locations, max_weight)

    def mutate(self, locations, mutation_rate=0.02):
        """遺伝子の変異を行う関数
    
        Args:
            gene (list[tuple[int, int]]): 現在の遺伝子。
            locations (list[Location]): 利用可能な拠点とアイテムのリスト。
            mutation_rate (float): 各要素に対する変異の確率。
            
        Returns:
            list[tuple[int, int]]: 変異後の遺伝子。
        """
        new_gene = self.gene.copy()
        used_locations = {loc_id for loc_id, _ in self.gene}  # 現在遺伝子に使われている拠点IDのセット
        
        for i in range(len(new_gene)):
            if random.random() <= mutation_rate:
                # 使用されていない拠点のリストを作成
                available_locations = [loc for loc in locations if loc.id not in used_locations]
                
                if available_locations:
                    # 使用されていない拠点からランダムに選択
                    location = random.choice(available_locations)
                    # 選択した拠点のアイテムからランダムに一つ選ぶ
                    item = random.choice(location.items)
                    # 遺伝子の該当部分を新しい拠点IDとアイテムIDに置き換える
                    new_gene[i] = (location.id, item.id)
                    used_locations.add(location.id)  # 更新された拠点を追加
                else:
                    # 使用可能な拠点がない場合は、変異をスキップ
                    continue

        self.gene = new_gene
        