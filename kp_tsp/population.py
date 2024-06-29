import random

from .individual import Individual

population_type = list[Individual]

class Population:
    """
    このクラスは個体群を管理します。
    属性:
    individuals: 個体のリストです。
    メソッド:
    evaluate(): 全個体の適合度を計算します。
    select(): 選択操作を行い、次世代に進む個体を選びます。
    crossover(): 交叉を行い、新たな個体を生成します。
    mutate(): 突然変異を個体群に適用します。
    generate_new_population(): 選択、交叉、突然変異を通じて新たな個体群を生成します。
    """

    def __init__(self, size, max_place) -> None:
        """
        個体群を初期化
        """
        self.individuals: population_type = [Individual(max_place) for _ in range(size)]

    def evaluate(self, locations, max_weight):
        """
        
        """
        for individual in self.individuals:
            individual.evaluate_fitness(locations, max_weight)
    
    def select(self):
        # トーナメント選択を使用して次世代の親を選択
        selected = []
        tournament_size = 3
        for _ in range(len(self.individuals)):
            contenders = random.sample(self.individuals, tournament_size)
            selected.append(max(contenders, key=lambda ind: ind.fitness))
        self.individuals = selected

    def crossover(self, parent1: Individual, parent2: Individual)->Individual:
        """
        一様交叉
        https://chatgpt.com/share/1f369666-fe20-4f75-bd92-423cb9990011
        : praram parent1: 交叉での親1
        : praram parent2: 交叉での親2
        : return : 交叉後の子
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
        if len(parent1.gene) > min_length:
            child.gene.extend(parent1.gene[min_length:])
        elif len(parent2.gene) > min_length:
            child.gene.extend(parent2.gene[min_length:])
        return child
    
    def mutate(self, mutation_rate):
        # 全個体に突然変異を適用
        for individual in self.individuals:
            individual.mutate(mutation_rate)

    def generate_new_population(self, crossover_rate):
        new_generation = []
        while len(new_generation) < len(self.individuals):
            parent1 = random.choice(self.individuals)
            parent2 = random.choice(self.individuals)
            if random.random() < crossover_rate:
                new_generation.append(self.crossover(parent1, parent2))
            else:
                new_generation.extend([parent1, parent2])
        self.individuals = new_generation[:len(self.individuals)]
    
