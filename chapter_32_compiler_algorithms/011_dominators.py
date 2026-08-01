"""使用不动点迭代计算控制流图的支配节点与立即支配节点。

适用场景：SSA 构造、循环检测和代码移动。核心思想：除入口外，节点的支配集是所有前驱支配集的交集再加自身。
输入输出：输入入口和 ``节点 -> 后继`` CFG，输出支配集或立即支配节点。时间 O(V²E)，空间 O(V²)。
边界：不可达节点不会进入结果；入口的立即支配节点为 ``None``。
"""

from __future__ import annotations


def compute_dominators(entry: int, cfg: dict[int, set[int]]) -> dict[int, set[int]]:
    """计算所有从入口可达节点的支配集。

    参数：入口与 CFG。返回值：节点到支配它的节点集合。关键点：交集表达所有路径都必须经过的节点。
    """
    reachable = _reachable(entry, cfg)
    predecessors = {node: set() for node in reachable}
    for source in reachable:
        for target in cfg.get(source, set()):
            if target in reachable:
                predecessors[target].add(source)
    dominators = {
        node: ({entry} if node == entry else set(reachable)) for node in reachable
    }
    changed = True
    while changed:
        changed = False
        for node in reachable - {entry}:
            incoming = predecessors[node]
            common = (
                set.intersection(*(dominators[parent] for parent in incoming))
                if incoming
                else set()
            )
            updated = common | {node}
            if updated != dominators[node]:
                dominators[node] = updated
                changed = True
    return dominators


def immediate_dominators(entry: int, cfg: dict[int, set[int]]) -> dict[int, int | None]:
    """由支配集推导每个节点唯一的立即支配节点。

    返回值中入口映射到 ``None``。关键点：立即支配节点是严格支配者中最靠近该节点者。
    """
    dominators = compute_dominators(entry, cfg)
    result = {entry: None}
    for node, doms in dominators.items():
        if node == entry:
            continue
        strict = doms - {node}
        result[node] = next(
            candidate
            for candidate in strict
            if all(
                candidate not in dominators[other] - {other}
                for other in strict
                if other != candidate
            )
        )
    return result


def _reachable(entry: int, cfg: dict[int, set[int]]) -> set[int]:
    reached, pending = {entry}, [entry]
    while pending:
        node = pending.pop()
        for successor in cfg.get(node, set()):
            if successor not in reached:
                reached.add(successor)
                pending.append(successor)
    return reached


if __name__ == "__main__":
    graph = {0: {1, 2}, 1: {3}, 2: {3}, 3: {4}, 4: {3}, 9: set()}
    dominators = compute_dominators(0, graph)
    assert dominators[3] == {0, 3}
    assert dominators[4] == {0, 3, 4}
    assert 9 not in dominators
    assert immediate_dominators(0, graph) == {0: None, 1: 0, 2: 0, 3: 0, 4: 3}
    print("011_dominators: all examples passed")
