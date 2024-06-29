import pytest

from kp_tsp.environment_models import Item, Location
from kp_tsp.fitness import calculate_distance, calculate_fitness

@pytest.fixture
def mock_locations():
    return [
        Location(id=1, items=[Item(id=1, weight=5, value=10), Item(id=2, weight=6, value=9), Item(id=3, weight=2, value=7)], coordinates=(20, 40)),
        Location(id=2, items=[Item(id=4, weight=5, value=8), Item(id=5, weight=3, value=6), Item(id=1, weight=5, value=10)], coordinates=(50, 1)),
        Location(id=3, items=[Item(id=6, weight=11, value=8), Item(id=7, weight=11, value=11), Item(id=7, weight=11, value=11)], coordinates=(50, 1)),
    ]

# 距離計算のテストケース
def test_calculate_distance():
    point1 = (100, 200)
    point2 = (200, 300)
    expected_distance = 141.4213562373095  # sqrt((200-100)^2 + (300-200)^2)
    calculated_distance = calculate_distance(point1, point2)
    assert calculated_distance == pytest.approx(expected_distance), "Distance calculation should be correct"

# 適応度計算
def test_calculate_fitness(mock_locations):
    # 重量制限内での適応度計算
    gene_within_weight_limit = [(1, 1), (2, 5)]
    max_weight = 15
    fitness = calculate_fitness(gene_within_weight_limit, mock_locations, max_weight)
    assert fitness > 0, "Fitness should be positive when weight is within the limit"

    # 重量オーバーの場合の適応度計算
    gene_over_weight_limit = [(1, 1), (3, 6)]
    fitness_over_weight = calculate_fitness(gene_over_weight_limit, mock_locations, max_weight)
    assert fitness_over_weight == 0, "Fitness should be zero when weight exceeds the limit"