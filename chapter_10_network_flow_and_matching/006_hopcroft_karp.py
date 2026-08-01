"""手写 Hopcroft-Karp 算法求二分图最大匹配。

适用场景：
- 左右两侧顶点明确分组，边只从左侧连接到右侧；
- 需要比朴素 DFS 增广路更高效地求最大匹配。

核心思想：
- 先用 BFS 在交替图中分层，得到最短增广路长度；
- 再用 DFS 只沿层次递增方向寻找一批点互不冲突的最短增广路；
- 一轮可以同时增广多条路径，因此总复杂度优于逐条增广。

输入输出：
- 输入为 `graph`，表示左侧顶点到右侧邻居列表的映射；
- 输出为 `右侧顶点 -> 左侧顶点` 的最大匹配字典。

时间复杂度：O(E * sqrt(V))
空间复杂度：O(V + E)

关键边界情况：
- 空图直接返回空匹配；
- 某些左侧顶点没有邻居时不会报错；
- 重复边不会破坏正确性，但会带来重复扫描成本；
- 本实现假设输入确实是二分图的左到右邻接表示。
"""

from __future__ import annotations

from collections import deque


def hopcroft_karp(graph: dict[str, list[str]]) -> dict[str, str]:
    """返回二分图最大匹配。

    参数：
    - graph：左侧顶点到右侧邻居列表的映射。

    返回值：
    - `右侧顶点 -> 左侧顶点` 的最大匹配结果。

    边界情况：
    - 空字典返回空匹配；
    - 左侧顶点对应空邻接表时，会被视作无法匹配的顶点。

    关键算法点：
    - BFS 负责构建“最短增广路层次图”；
    - DFS 只在层次图中向前推进，保证一次 BFS 后能批量找到最短增广路。
    """

    left_match: dict[str, str | None] = {left: None for left in graph}
    right_vertices = {right for neighbors in graph.values() for right in neighbors}
    right_match: dict[str, str | None] = {right: None for right in right_vertices}
    distance: dict[str, int] = {}
    infinity = float("inf")

    def bfs() -> bool:
        """构造层次图，并判断是否还存在增广路。"""

        queue: deque[str] = deque()

        for left in graph:
            if left_match[left] is None:
                distance[left] = 0
                queue.append(left)
            else:
                distance[left] = infinity

        found_augmenting_path = False

        while queue:
            left = queue.popleft()

            # 只有当前点仍可能位于最短增广路上，才继续向外扩展。
            for right in graph[left]:
                matched_left = right_match.get(right)
                if matched_left is None:
                    found_augmenting_path = True
                elif distance[matched_left] == infinity:
                    distance[matched_left] = distance[left] + 1
                    queue.append(matched_left)

        return found_augmenting_path

    def dfs(left: str) -> bool:
        """在层次图中寻找一条从 `left` 出发的增广路。"""

        for right in graph[left]:
            matched_left = right_match.get(right)

            # 遇到未匹配右点，或能沿最短层次继续重排已有匹配时即可增广。
            if matched_left is None or (
                distance[matched_left] == distance[left] + 1 and dfs(matched_left)
            ):
                left_match[left] = right
                right_match[right] = left
                return True

        # 该点在本轮层次图中已无法通往汇侧，后续 DFS 不必再次尝试。
        distance[left] = infinity
        return False

    while bfs():
        for left in graph:
            if left_match[left] is None:
                dfs(left)

    return {
        right: left
        for right, left in right_match.items()
        if left is not None
    }


if __name__ == "__main__":
    matching = hopcroft_karp(
        {
            "u1": ["v1", "v2"],
            "u2": ["v1", "v3"],
            "u3": ["v2"],
            "u4": ["v3", "v4"],
        }
    )
    assert len(matching) == 4
    assert set(matching.values()) == {"u1", "u2", "u3", "u4"}

    assert hopcroft_karp({}) == {}
    assert hopcroft_karp({"left": []}) == {}

    partial_matching = hopcroft_karp(
        {
            "a": ["1"],
            "b": ["1"],
            "c": ["2"],
        }
    )
    assert len(partial_matching) == 2
    assert set(partial_matching.keys()) == {"1", "2"}

    print("006_hopcroft_karp: all examples passed")
