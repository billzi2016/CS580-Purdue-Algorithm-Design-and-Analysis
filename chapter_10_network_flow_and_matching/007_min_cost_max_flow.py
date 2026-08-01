"""手写最小费用最大流的逐次最短增广路算法。

适用场景：
- 有容量限制的有向网络；
- 每条边既有容量也有单位费用；
- 需要在最大流或给定流量上限下，使总费用最小。

核心思想：
- 维护残量网络；
- 每轮在残量网络里寻找一条从源到汇的最短费用增广路；
- 沿该路径增广尽可能多的流量，并同步更新反向边；
- 当不存在可达路径时，已经得到在当前可发送总流量下的最小费用流。

输入输出：
- 先逐条加入边 `(u, v, capacity, cost)`；
- 再调用 `min_cost_max_flow(source, sink, flow_limit)`；
- 输出总流量与总费用。

时间复杂度：
- Bellman-Ford 版本单轮最短路为 O(VE)；
- 最多增广 O(F) 轮，因此总复杂度可写作 O(FVE)，其中 F 为增广轮数。

空间复杂度：O(V + E)

关键边界情况：
- 不存在从源到汇的路径时返回 0 流 0 费用；
- `flow_limit` 为 0 时直接返回；
- 允许负费用边，但假设不存在可被利用的负费用环；
- 容量必须非负，顶点编号必须在范围内。
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class _ResidualEdge:
    """残量网络中的一条边。"""

    to: int
    reverse_index: int
    capacity: float
    cost: float


@dataclass(frozen=True)
class FlowCostResult:
    """最小费用流结果。"""

    flow: float
    cost: float


class MinCostMaxFlow:
    """最小费用最大流求解器。"""

    def __init__(self, vertex_count: int) -> None:
        """初始化残量网络。

        参数：
        - vertex_count：顶点数量，顶点编号范围为 `[0, vertex_count)`.

        返回值：
        - 无。

        边界情况：
        - 顶点数小于等于 0 时抛出异常。

        关键算法点：
        - 每条原始边都会配套创建一条费用取反、初始容量为 0 的反向边。
        """

        if vertex_count <= 0:
            raise ValueError("顶点数量必须为正整数")

        self.vertex_count = vertex_count
        self.graph: list[list[_ResidualEdge]] = [[] for _ in range(vertex_count)]

    def add_edge(self, source: int, target: int, capacity: float, cost: float) -> None:
        """向网络中加入一条有向边。

        参数：
        - source：起点编号；
        - target：终点编号；
        - capacity：边容量，必须非负；
        - cost：单位流量经过该边的费用。

        返回值：
        - 无。

        边界情况：
        - 顶点越界或容量为负时抛出异常；
        - 容量为 0 的边会被保留，但永远不会参与正向增广。

        关键算法点：
        - 反向边的费用必须取负，才能在撤销部分流量时正确修正总费用。
        """

        if not 0 <= source < self.vertex_count:
            raise ValueError("source 超出顶点范围")
        if not 0 <= target < self.vertex_count:
            raise ValueError("target 超出顶点范围")
        if capacity < 0:
            raise ValueError("容量不能为负数")

        forward = _ResidualEdge(
            to=target,
            reverse_index=len(self.graph[target]),
            capacity=capacity,
            cost=cost,
        )
        backward = _ResidualEdge(
            to=source,
            reverse_index=len(self.graph[source]),
            capacity=0,
            cost=-cost,
        )
        self.graph[source].append(forward)
        self.graph[target].append(backward)

    def min_cost_max_flow(
        self,
        source: int,
        sink: int,
        flow_limit: float | None = None,
    ) -> FlowCostResult:
        """计算从源点到汇点的最小费用最大流。

        参数：
        - source：源点编号；
        - sink：汇点编号；
        - flow_limit：若给定，则只发送不超过该上限的流量。

        返回值：
        - `FlowCostResult(flow, cost)`，分别表示实际发送的流量和总费用。

        边界情况：
        - 当源点等于汇点时抛出异常；
        - `flow_limit` 为 `None` 时，会尽可能发送最大流；
        - `flow_limit` 为 0 时直接返回零结果。

        关键算法点：
        - 使用 Bellman-Ford 在残量网络里找最短费用增广路；
        - 通过记录前驱顶点和前驱边索引，回溯出本轮可增广的瓶颈容量。
        """

        if not 0 <= source < self.vertex_count:
            raise ValueError("source 超出顶点范围")
        if not 0 <= sink < self.vertex_count:
            raise ValueError("sink 超出顶点范围")
        if source == sink:
            raise ValueError("source 和 sink 不能相同")
        if flow_limit is not None and flow_limit < 0:
            raise ValueError("flow_limit 不能为负数")
        if flow_limit == 0:
            return FlowCostResult(flow=0, cost=0)

        target_flow = float("inf") if flow_limit is None else flow_limit
        total_flow = 0.0
        total_cost = 0.0

        while total_flow < target_flow:
            distance = [float("inf")] * self.vertex_count
            previous_vertex = [-1] * self.vertex_count
            previous_edge = [-1] * self.vertex_count
            distance[source] = 0.0

            # Bellman-Ford 会逐步松弛所有仍有残量的边，允许处理负费用边。
            for _ in range(self.vertex_count - 1):
                updated = False

                for vertex in range(self.vertex_count):
                    if distance[vertex] == float("inf"):
                        continue

                    for edge_index, edge in enumerate(self.graph[vertex]):
                        if edge.capacity <= 0:
                            continue

                        candidate_cost = distance[vertex] + edge.cost
                        if candidate_cost < distance[edge.to]:
                            distance[edge.to] = candidate_cost
                            previous_vertex[edge.to] = vertex
                            previous_edge[edge.to] = edge_index
                            updated = True

                if not updated:
                    break

            if distance[sink] == float("inf"):
                break

            augment_flow = target_flow - total_flow
            vertex = sink

            while vertex != source:
                parent = previous_vertex[vertex]
                edge = self.graph[parent][previous_edge[vertex]]
                augment_flow = min(augment_flow, edge.capacity)
                vertex = parent

            vertex = sink
            while vertex != source:
                parent = previous_vertex[vertex]
                edge_index = previous_edge[vertex]
                edge = self.graph[parent][edge_index]
                reverse_edge = self.graph[edge.to][edge.reverse_index]

                edge.capacity -= augment_flow
                reverse_edge.capacity += augment_flow
                vertex = parent

            total_flow += augment_flow
            total_cost += augment_flow * distance[sink]

        return FlowCostResult(flow=total_flow, cost=total_cost)


if __name__ == "__main__":
    solver = MinCostMaxFlow(4)
    solver.add_edge(0, 1, 2, 1)
    solver.add_edge(0, 2, 1, 2)
    solver.add_edge(1, 2, 1, 0)
    solver.add_edge(1, 3, 1, 3)
    solver.add_edge(2, 3, 2, 1)

    result = solver.min_cost_max_flow(0, 3)
    assert result == FlowCostResult(flow=3.0, cost=9.0)

    limited_solver = MinCostMaxFlow(4)
    limited_solver.add_edge(0, 1, 2, 1)
    limited_solver.add_edge(0, 2, 1, 2)
    limited_solver.add_edge(1, 2, 1, 0)
    limited_solver.add_edge(1, 3, 1, 3)
    limited_solver.add_edge(2, 3, 2, 1)

    limited_result = limited_solver.min_cost_max_flow(0, 3, flow_limit=2)
    assert limited_result == FlowCostResult(flow=2.0, cost=5.0)

    disconnected_solver = MinCostMaxFlow(3)
    disconnected_solver.add_edge(0, 1, 5, 2)
    assert disconnected_solver.min_cost_max_flow(0, 2) == FlowCostResult(flow=0.0, cost=0.0)

    print("007_min_cost_max_flow: all examples passed")
