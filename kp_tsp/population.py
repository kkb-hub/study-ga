import random

from kp_tsp.environment_models import Location
from .individual import Individual

population_type = list[Individual]

class Population:
    """
    遺伝子の個体群の管理

    Attributes
    ----------
    individuals : population_type
       遺伝子の個体群群
    """ 

    def __init__(self, size, max_place) -> None:
        """
        個体群を初期化
        """
        self.individuals: population_type = [Individual(max_place) for _ in range(size)]

    def evaluate(self, locations: list[Location], max_weight: int):
        """
        適応度計算を各個体に行わせる

        Parameters
        ----------
        location : list[Locations]
            拠点数
        max_weigth : int
            ナップサックの許容値
        """
        for individual in self.individuals:
            individual.evaluate_fitness(locations, max_weight)
    
    def select(self):
        """
        トーナメント選択を使用して次世代の親を選択
        """
        selected = []
        tournament_size = 3
        for _ in range(len(self.individuals)):
            contenders = random.sample(self.individuals, tournament_size)
            selected.append(max(contenders, key=lambda ind: ind.fitness))
        self.individuals = selected

    def crossover(self, parent1: Individual, parent2: Individual)->Individual:
        """
        一様交叉
        
        : praram parent1: 交叉での親1
        : praram parent2: 交叉での親2
        : return : 交叉後の子
        """
        """
        交叉関数
        今回は一様交叉
        https://chatgpt.com/share/1f369666-fe20-4f75-bd92-423cb9990011

        Parameters
        ----------
        parent1 : Individual
            親
        parent2 : Individual
            親2

        Returns
        -------
        子 : Individual
            交叉後の個体
        """
        child = Individual()

        # 最短の親を基準に選択
        min_length = min(len(parent1.gene), len(parent2.gene))
        for i in range(min_length):
            if random.random() < 0.5:
                child.gene.append(parent1.gene[i])
            else:
                child.gene.append(parent2.gene[i])

        # 残りの遺伝子を長い親から受け継ぐ
        # ただし、1/2の確率とする。確率を決めないと遺伝子が無限に伸びるため。
        if random.random() < 0.01:
            if len(parent1.gene) > min_length:
                child.gene.extend(parent1.gene[min_length:])
            elif len(parent2.gene) > min_length:
                child.gene.extend(parent2.gene[min_length:])
                
        return child
    
    def mutate(self, mutation_rate):
        """
        突然変異を各個体に行わせる

        Parameters
        ----------
        mutation_rate : float
            各遺伝子の突然変異確率
        """
        for individual in self.individuals:
            individual.mutate(mutation_rate)
            individual.shave_gene()

    def generate_new_population(self, crossover_rate):
        """
        次世代の個体群を作成

        Parameters
        ----------
        crossover_rate : float
            選択された親のペアが、実際に交叉される確率
        """
        new_generation = []
        while len(new_generation) < len(self.individuals):
            parent1 = random.choice(self.individuals)
            parent2 = random.choice(self.individuals)
            if random.random() < crossover_rate:
                new_generation.append(self.crossover(parent1, parent2))
            else:
                new_generation.extend([parent1, parent2])
        self.individuals = new_generation[:len(self.individuals)]
    
