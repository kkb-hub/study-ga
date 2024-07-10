import matplotlib.pyplot as plt

from kp_tsp.individual import Individual
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
    def __init__(self, population_size, num_place, max_generations, crossover_rate_inlist = 0.8, crossover_rate_intuple = 0.8, mutation_rate = 0.02):
        self.population = Population(population_size, num_place)
        self.max_generations = max_generations
        self.crossover_rate_inlist = crossover_rate_inlist
        self.crossover_rate_intuple = crossover_rate_intuple
        self.mutation_rate = mutation_rate
        self.current_generation = 0

    def run(self, locations):
        # 初期個体群の評価
        self.population.evaluate(locations)

        # 最大世代数に達するまで進化を続ける
        while self.current_generation < self.max_generations:
            # print(f"Gen. {self.current_generation}: Best Fitness = {self.get_best_fitness():.6f}")
            print(f"Gen. {self.current_generation}- Best Fitness: {self.get_best_individual().fitness:.6f}, dist: {self.get_best_individual().total_dist: .0f}, inversed value: {self.get_best_individual().total_value_inverse}")
             # 100の倍数の世代でのみ描画
            if self.current_generation % 100 == 0:
                self.plot_best_individual(self.get_best_individual().gene, locations, self.current_generation)
            self.population.generate_new_population(self.crossover_rate_inlist, self.crossover_rate_intuple)
            self.population.evaluate(locations)
            self.current_generation += 1

        best_individual = self.get_best_individual()
        return best_individual

    def get_best_fitness(self):
        # 最も適合度の高い個体を見つける
        return min(individual.fitness for individual in self.population.individuals)

    def get_best_individual(self):
        # 最も適合度の高い個体を返す
        return min(self.population.individuals, key=lambda ind: ind.fitness)
    
    def plot_best_individual(self, gene: list, locations, generation):
        fig, ax = plt.subplots()
        x_coords = []
        y_coords = []
        
        # 訪問した場所の座標を収集
        for gene_tuple in gene:
            visited, loc_id, item_id = gene_tuple
            if visited:
                loc = next(loc for loc in locations if loc.id == loc_id)
                x_coords.append(loc.coordinates[0])
                y_coords.append(loc.coordinates[1])
                ax.plot(loc.coordinates[0], loc.coordinates[1], 'bo')  # 'bo' = blue circle
                ax.text(loc.coordinates[0], loc.coordinates[1], f"{loc_id}\nItem: {item_id}", fontsize=12, ha='center')
        
        # 訪問した場所を線で結ぶ
        ax.plot(x_coords, y_coords, 'b-')  # 'b-' = blue line

        ax.set_xlabel('X Coordinate')
        ax.set_ylabel('Y Coordinate')
        ax.set_title('Map of Visited Locations and Collected Items')
        
        # グラフをファイルに保存
        plt.savefig(f"./image/gen-{generation}.png")
        plt.close(fig)  # フィギュアをクローズ

