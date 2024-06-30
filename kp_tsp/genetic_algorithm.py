from .population import Population

class GeneticAlgorithm:
    """
    遺伝的アルゴリズムを利用して最適化問題を解くためのクラスです。
    このクラスは個体群の進化プロセスを制御し、各世代において個体群の評価、選択、交叉、突然変異を行いながら最適な解を探求します。
    属性:
    population: 現在の個体群を保持します。
    generations: 世代数をカウントします。
    max_generations: 最大世代数です。
    メソッド:
    run(): アルゴリズムを実行し、最適な解を見つけます。各世代において、個体群の評価、選択、交叉、突然変異を行います。
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
            print(f"Gen. {self.current_generation}: Best Fitness = {self.get_best_fitness():.6f}")
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
