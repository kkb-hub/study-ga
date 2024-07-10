import random
import math

import numpy as np

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
    
    def calculate_mean(self, data: list):
        return sum(data) / len(data)

    def calculate_std(self, data):
        mean = self.calculate_mean(data)
        variance = sum((x - mean) ** 2 for x in data) / len(data)  # 母集団標準偏差の場合
        return math.sqrt(variance)

    def evaluate(self, locations: list[Location]):
        """
        適応度計算を各個体に行わせる

        Parameters
        ----------
        location : list[Locations]
            拠点数
        """

        for ind in self.individuals:
            ind.calc_total(locations)
        
        total_distances = [ind.total_dist for ind in self.individuals]
        total_weights = [ind.total_weight for ind in self.individuals]
        total_values_inverse = [ind.total_value_inverse for ind in self.individuals]
        
        mean_distances = self.calculate_mean(total_distances)
        mean_weights = self.calculate_mean(total_weights)
        mean_value_inverse = self.calculate_mean(total_values_inverse)

        std_distances = self.calculate_std(total_distances)
        std_weights = self.calculate_std(total_weights)
        std_value_inverse = self.calculate_std(total_values_inverse)

        epsilon = 1e-8
        for ind in self.individuals:
            ind.normalized_dist = (ind.total_dist - mean_distances) / (std_distances + epsilon)
            ind.normalized_weight = (ind.total_weight - mean_weights) / (std_weights + epsilon)
            ind.normalized_value = (ind.total_value_inverse - mean_value_inverse) / (std_value_inverse + epsilon)
            ind.fitness = max(ind.normalized_dist, ind.normalized_weight, ind.normalized_value) * 100

        self.select()
    
    def select(self):
        """
        トーナメント選択を使用して次世代の親を選択
        """
        selected = []
        tournament_size = 3
        for _ in range(len(self.individuals)):
            contenders = random.sample(self.individuals, tournament_size)
            selected.append(min(contenders, key=lambda ind: ind.fitness))
        self.individuals = selected

    def crossover_inlist(self, parent1: Individual, parent2: Individual)->Individual:
        """
        List内要素に対する一様交叉、つまり、[(), (), ()]とタプルがリスト内に入っているが、そのタプルごと交差する。

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

        length = min(len(parent1.gene), len(parent2.gene))
        for i in range(length):
            if random.random() < 0.5:
                child.gene.append(parent1.gene[i])
            else:
                child.gene.append(parent2.gene[i])
                
        return child
    
    def crossover_intuple(self, parent1: Individual, parent2: Individual)->Individual:
        """
        List内のタプルに対する一様交叉。つまり、[(True, 4, 1), (), ()]の(True, 4, 1)の各要素を交差する。
        
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
        for gene1, gene2 in zip(parent1.gene, parent2.gene):
            num = random.random()
            if num < 0.25 :
                child.gene.append((gene1[0], gene1[1], gene1[2]))
            elif num < 0.5:
                child.gene.append((gene2[0], gene1[1], gene1[2]))
            elif num < 0.75:
                child.gene.append((gene1[0], gene1[1], gene2[2]))
            else:
                child.gene.append((gene2[0], gene1[1], gene2[2]))

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

    def generate_new_population(self, crossover_rate_inlist, crossover_rate_intuple):
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
            if random.random() < crossover_rate_inlist:
                new_generation.append(self.crossover_inlist(parent1, parent2))
            else:
                new_generation.extend([parent1, parent2])
            if random.random() < crossover_rate_intuple:
                new_generation.append(self.crossover_intuple(parent1, parent2))
            else:
                new_generation.extend([parent1, parent2])
        self.individuals = new_generation[:len(self.individuals)]
    
