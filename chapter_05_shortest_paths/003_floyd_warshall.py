"""
文件意图：
    本文件手写实现 Floyd-Warshall 算法，用于计算所有点对之间的最短路径。

适用场景：
    节点数量中等、需要任意两点最短距离，并且图中可以有负权边但不能有负权环。

核心思想：
    动态规划枚举中间点 k。dist[i][j] 表示只允许使用已处理过的中间点时，
    i 到 j 的最短距离；转移为 dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])。

输入输出：
    输入节点列表和边列表，返回距离矩阵字典。

时间复杂度：
    O(V^3)

空间复杂度：
    O(V^2)
"""

from collections.abc import Hashable

Node = Hashable
Edge = tuple[Node, Node, float]


def floyd_warshall(nodes: list[Node], edges: list[Edge]) -> dict[Node, dict[Node, float]]:
    """
    计算所有点对最短距离。

    参数：
        nodes: 节点列表。
        edges: 有向边列表，每条边为 (u, v, weight)。

    返回：
        dist[u][v] 表示 u 到 v 的最短距离。

    异常：
        如果存在负权环，抛出 ValueError。
    """
    dist = {start: {end: float("inf") for end in nodes} for start in nodes}

    for node in nodes:
        dist[node][node] = 0.0

    for start, end, weight in edges:
        # 多重边取较小权重，避免后出现的较大边覆盖较优边。
        dist[start][end] = min(dist[start][end], weight)

    for middle in nodes:
        for start in nodes:
            for end in nodes:
                candidate = dist[start][middle] + dist[middle][end]
                if candidate < dist[start][end]:
                    dist[start][end] = candidate

    for node in nodes:
        if dist[node][node] < 0:
            raise ValueError("图中存在负权环")

    return dist


if __name__ == "__main__":
    nodes = ["A", "B", "C", "D"]
    edges = [
        ("A", "B", 3),
        ("A", "C", 10),
        ("B", "C", -2),
        ("C", "D", 2),
        ("A", "D", 100),
    ]
    dist = floyd_warshall(nodes, edges)
    assert dist["A"]["A"] == 0.0
    assert dist["A"]["C"] == 1.0
    assert dist["A"]["D"] == 3.0
    assert dist["D"]["A"] == float("inf")

    multi_edge_dist = floyd_warshall(["A", "B"], [("A", "B", 5), ("A", "B", 2)])
    assert multi_edge_dist["A"]["B"] == 2

    try:
        floyd_warshall(["A", "B"], [("A", "B", -1), ("B", "A", -1)])
        raise AssertionError("负权环必须抛出 ValueError")
    except ValueError:
        pass

    print("003_floyd_warshall: all examples passed")
