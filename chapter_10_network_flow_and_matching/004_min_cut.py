"""以 Edmonds–Karp 残量网络求 s-t 最小割。

输入容量邻接矩阵、源点与汇点，输出最大流值和最小割两侧顶点。每轮 BFS 找增广路；结束后残量图中从源可达的顶点即割的一侧。时间 O(VE²)，空间 O(V²)。容量必须非负。
"""
from __future__ import annotations
from collections import deque
from dataclasses import dataclass

@dataclass(frozen=True)
class MinCutResult:
    value: float
    source_side: frozenset[int]
    sink_side: frozenset[int]

def minimum_cut(capacity: list[list[float]], source: int, sink: int) -> MinCutResult:
    """返回最小 s-t 割及其容量；输入为方阵，源汇必须不同。"""
    n = len(capacity)
    if n == 0 or any(len(row) != n or any(edge < 0 for edge in row) for row in capacity): raise ValueError("容量必须是非负方阵")
    residual = [row[:] for row in capacity]; flow = 0.0
    while True:
        parent = [-1] * n; parent[source] = source; queue = deque([source])
        while queue and parent[sink] < 0:
            node = queue.popleft()
            for nxt, edge in enumerate(residual[node]):
                if edge > 0 and parent[nxt] < 0: parent[nxt] = node; queue.append(nxt)
        if parent[sink] < 0: break
        amount = float("inf"); node = sink
        while node != source: amount = min(amount, residual[parent[node]][node]); node = parent[node]
        node = sink
        while node != source: residual[parent[node]][node] -= amount; residual[node][parent[node]] += amount; node = parent[node]
        flow += amount
    reached, queue = {source}, deque([source])
    while queue:
        node = queue.popleft()
        for nxt, edge in enumerate(residual[node]):
            if edge > 0 and nxt not in reached: reached.add(nxt); queue.append(nxt)
    return MinCutResult(flow, frozenset(reached), frozenset(set(range(n)) - reached))

if __name__ == "__main__":
    result = minimum_cut([[0, 3, 2, 0], [0, 0, 1, 2], [0, 0, 0, 3], [0, 0, 0, 0]], 0, 3)
    assert result.value == 5 and result.source_side == frozenset({0})
    print("004_min_cut: all examples passed")
