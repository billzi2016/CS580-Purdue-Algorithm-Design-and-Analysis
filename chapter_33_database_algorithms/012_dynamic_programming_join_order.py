"""
动态规划 Join Ordering：用 Selinger 风格 DP 搜索左深连接顺序。

意图：展示查询优化器如何用代价模型选择多表 join 顺序。
"""

from itertools import combinations


def optimize_join_order(table_sizes: dict[str, int], selectivities: dict[frozenset[str], float]) -> tuple[list[str], float]:
    """返回估计代价最低的左深 join 顺序和代价。"""

    tables = sorted(table_sizes)
    dp: dict[frozenset[str], tuple[list[str], float, float]] = {}
    for table in tables:
        subset = frozenset([table])
        dp[subset] = ([table], 0.0, float(table_sizes[table]))

    for size in range(2, len(tables) + 1):
        for combo in combinations(tables, size):
            subset = frozenset(combo)
            best_order: list[str] = []
            best_cost = float("inf")
            best_cardinality = 0.0
            for last in combo:
                previous = subset - {last}
                prev_order, prev_cost, prev_cardinality = dp[previous]
                join_cardinality = prev_cardinality * table_sizes[last] * _selectivity(previous, last, selectivities)
                cost = prev_cost + join_cardinality
                if cost < best_cost:
                    best_order = prev_order + [last]
                    best_cost = cost
                    best_cardinality = join_cardinality
            dp[subset] = (best_order, best_cost, best_cardinality)

    order, cost, _ = dp[frozenset(tables)]
    return order, cost


def _selectivity(existing: frozenset[str], new_table: str, selectivities: dict[frozenset[str], float]) -> float:
    value = 1.0
    for table in existing:
        value *= selectivities.get(frozenset([table, new_table]), 1.0)
    return value


if __name__ == "__main__":
    sizes = {"A": 1000, "B": 100, "C": 10}
    sels = {frozenset(["A", "B"]): 0.01, frozenset(["B", "C"]): 0.1, frozenset(["A", "C"]): 0.5}
    order, cost = optimize_join_order(sizes, sels)
    assert order == ["C", "B", "A"]
    assert cost == 600.0

    print("012_dynamic_programming_join_order: all examples passed")
