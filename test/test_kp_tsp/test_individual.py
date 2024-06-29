import unittest

import pytest

from kp_tsp.individual import Individual
from kp_tsp.environment_models import Item, Location

def create_mock_location(location_id: int, num_items: int, coords: tuple[int, int]) -> Location:
    items = [Item(id=i, weight=i * 2, value=i * 3) for i in range(1, num_items + 1)]
    return Location(id=location_id, items=items, coordinates=coords)

# このテストではrandomモジュールの挙動を予測可能にするためにパッチを適用する
@pytest.fixture
def fixed_random(monkeypatch):
    monkeypatch.setattr('kp_tsp.individual.random.randint', lambda a, b: a)  # 最小値を返すように固定
    monkeypatch.setattr('kp_tsp.individual.random.sample', lambda population, k: population[:k])  # 最初のk要素を返す
    monkeypatch.setattr('kp_tsp.individual.random.choice', lambda seq: seq[0])  # 最初の要素を選択
    # monkeypatch.setattr('kp_tsp.individual.random.random', lambda a, b: a)  # 最初の要素を選択


# コンストラクタのテスト
def test_constructor(fixed_random):
    individual = Individual()
    assert individual.gene == []
    assert individual.fitness == 0

    individual_with_max = Individual(max_place=10)
    # 拠点数に応じてgeneが初期化されるか
    assert len(individual_with_max.gene) == 2  # randint(10//4, 10//2) => 2 (mocked)
    assert all(isinstance(x, tuple) and len(x) == 2 for x in individual_with_max.gene)

# 遺伝子初期化のテスト
def test_initialize_gene(fixed_random):
    individual = Individual(max_place=10)
    # 指定された範囲内でランダムな遺伝子が生成されるか
    expected_gene_length = 10 // 4
    assert len(individual.gene) == expected_gene_length

# 遺伝子の変異テスト
def test_mutate(fixed_random):
    individual = Individual(max_place=10)
    original_gene = individual.gene.copy()
    locations = [create_mock_location(location_id=i, num_items=5, coords=(x, x)) for i, x in enumerate(range(1, 100))]
    individual.mutate(locations, mutation_rate=1.0)  # 100% 変異率を設定してテスト
    # 変異後の遺伝子が変更されているかどうかを確認
    assert individual.gene != original_gene  # 変更点の確認