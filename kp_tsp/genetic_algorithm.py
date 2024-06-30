from .population import Population

class GeneticAlgorithm:
    """
    遺伝的アルゴリズムを動作させるクラス
    
    Attributes
    ----------
    population : Population
        現在の世代の個体群
    max_generations: int
        アルゴリズムの最大世代数
    crossover_rate : float
        選ばれた親のペアが交叉を行う確率
    mutation_rate : float
        突然変異の確率
    current_generation : int
        現在の世代数
    """
    def __init__(self, population_size, num_place, max_generations, crossover_rate = 0.8, mutation_rate = 0.02):
        self.population = Population(population_size, num_place)
        self.max_generations = max_generations
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.current_generation = 0

    def run(self, locations, max_weight):
        # 初期個体群の評価
        self.population.evaluate(locations, max_weight)

        # 最大世代数に達するまで進化を続ける
        while self.current_generation < self.max_generations:
            # print(f"Gen. {self.current_generation}: Best Fitness = {self.get_best_fitness():.6f}")
            print(f"Gen. {self.current_generation}- Best Fitness: {self.get_best_individual().fitness:.6f}, dist: {self.get_best_individual().total_dist: .0f}, value: {self.get_best_individual().total_value}")
            self.population.generate_new_population(self.crossover_rate)
            self.population.evaluate(locations, max_weight)
            self.current_generation += 1

        best_individual = self.get_best_individual()
        return best_individual

    def get_best_fitness(self):
        # 最も適合度の高い個体を見つける
        return max(individual.fitness for individual in self.population.individuals)

    def get_best_individual(self):
        # 最も適合度の高い個体を返す
        return max(self.population.individuals, key=lambda ind: ind.fitness)
