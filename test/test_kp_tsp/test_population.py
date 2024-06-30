import pytest
import random

from kp_tsp.individual import Individual
from kp_tsp.population import Population
from kp_tsp.environment_models import Item, Location

@pytest.fixture
def population():
    return Population(10,12) # size=10, max_place=5のPopulationインスタンスを生成

@pytest.fixture
def max_weight():
    return 10

@pytest.fixture
def locations():
    items1 = [Item(id=1, weight=2, value=3), Item(id=2, weight=1, value=2)]
    items2 = [Item(id=3, weight=3, value=4), Item(id=4, weight=1, value=1)]
    return [Location(id=1, items=items1, coordinates=(2, 5)),
            Location(id=2, items=items2, coordinates=(1, 1))]

# @pytest.fixture
# def individuals():
#     return [MockIndividual() for _ in range(10)]

# コンストラクタのテスト
def test_constructor(population):
    assert len(population.individuals) == 10 # 10個の遺伝子Listが作成されているか
    assert all(isinstance(ind, Individual) for ind in population.individuals) # リストの中身がすべてIndividual型か

# Selectionテスト
# ロジックのテストが必要
def test_population_select(population):
    # 初期フィットネスを設定
    for ind in population.individuals:
        ind.fitness = random.randint(1, 100)
    population.select()
    # 選択された個体が元のリストに含まれているか確認
    selected_fitnesses = {ind.fitness for ind in population.individuals}
    assert len(selected_fitnesses) <= len(population.individuals)

# Crossoverテスト
# ロジックのテストが必要
def test_population_crossover(population):
    parent1 = Individual(max_place=5)
    parent2 = Individual(max_place=5)
    child = population.crossover(parent1, parent2)
    assert isinstance(child, Individual)
    assert len(child.gene) <= max(len(parent1.gene), len(parent2.gene))

# New Population Generationテスト
# ロジックのテストが必要
def test_population_generate_new_population(population):
    initial_size = len(population.individuals)
    population.generate_new_population(0.5)
    assert len(population.individuals) == initial_size