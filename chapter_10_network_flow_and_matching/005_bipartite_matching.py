"""用 DFS 增广路求二分图最大匹配。

输入左侧顶点到右侧邻居的字典，输出左右匹配。每轮为一个未匹配左点寻找交替增广路。时间 O(VE)，空间 O(V)。重复边不影响结果。
"""

from __future__ import annotations


def maximum_bipartite_matching(graph: dict[str, list[str]]) -> dict[str, str]:
    """返回 ``右侧顶点 -> 左侧顶点`` 的最大匹配。"""
    matched: dict[str, str] = {}

    def augment(left: str, seen: set[str]) -> bool:
        for right in graph[left]:
            if right in seen:
                continue
            seen.add(right)
            if right not in matched or augment(matched[right], seen):
                matched[right] = left
                return True
        return False

    for left in graph:
        augment(left, set())
    return matched


if __name__ == "__main__":
    matching = maximum_bipartite_matching(
        {"a": ["1", "2"], "b": ["1"], "c": ["2", "3"]}
    )
    assert len(matching) == 3 and set(matching.values()) == {"a", "b", "c"}
    assert maximum_bipartite_matching({}) == {}
    print("005_bipartite_matching: all examples passed")
