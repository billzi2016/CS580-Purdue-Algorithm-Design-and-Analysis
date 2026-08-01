"""Neighbor Joining 系统发育树的教学实现。

适用场景：
- 已知样本间距离矩阵，但不假设严格分子钟；
- 需要根据距离构建一棵非定根系统发育树；
- 更关注拓扑与分支长度的恢复，而不是 ultrametric 层次聚类。

核心思想：
- 每轮计算 Q 矩阵，校正各节点到其余节点的总距离；
- 选择 Q 值最小的一对邻居作为新的“樱桃”合并；
- 根据标准公式计算两条肢长，并更新新节点到其他节点的距离；
- 直到只剩两个节点时结束。

输入输出：
- 输入：样本标签列表与对称距离矩阵；
- 输出：一棵带分支长度的 rooted 表示树，根节点只作为最终拼接容器使用。

时间复杂度：O(n^3)
空间复杂度：O(n^2)

关键边界情况：
- 空标签列表会抛出异常；
- 两个标签时直接返回一条二叉连接；
- 距离矩阵必须对称、非负、对角线为 0；
- 这是教学版 NJ，不处理负枝长再优化、缺失距离和大型启发式加速。
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class NJNode:
    """Neighbor Joining 树节点。"""

    name: str
    left: NJNode | None = None
    right: NJNode | None = None
    left_length: float = 0.0
    right_length: float = 0.0
    members: tuple[str, ...] = ()


def neighbor_joining_tree(labels: list[str], distances: dict[tuple[str, str], float]) -> NJNode:
    """用 Neighbor Joining 算法构建系统发育树。

    参数：
    - labels：叶子标签列表；
    - distances：无向距离矩阵。

    返回值：
    - NJ 树的根节点。

    边界情况：
    - 空标签抛出异常；
    - 单个标签返回叶节点；
    - 两个标签直接连边。

    关键算法点：
    - Q 矩阵通过扣除总距离项，把“整体偏远”的样本影响消掉；
    - 合并时必须先用原矩阵算枝长，再用公式更新新节点距离。
    """

    if not labels:
        raise ValueError("labels 不能为空")
    if len(set(labels)) != len(labels):
        raise ValueError("labels 不能包含重复项")

    _validate_distance_matrix(labels, distances)

    active_nodes: dict[str, NJNode] = {
        label: NJNode(name=label, members=(label,))
        for label in labels
    }
    current_distances = {
        frozenset({left, right}): _distance_between(left, right, distances)
        for index, left in enumerate(labels)
        for right in labels[index + 1 :]
    }
    next_internal_id = 1

    if len(active_nodes) == 1:
        return next(iter(active_nodes.values()))

    while len(active_nodes) > 2:
        names = list(active_nodes)
        total_distance = {
            name: sum(
                current_distances[frozenset({name, other})]
                for other in names
                if other != name
            )
            for name in names
        }
        remaining = len(names)

        left_name, right_name = min(
            (
                (left, right)
                for index, left in enumerate(names)
                for right in names[index + 1 :]
            ),
            key=lambda pair: (
                (remaining - 2) * current_distances[frozenset(pair)]
                - total_distance[pair[0]]
                - total_distance[pair[1]],
                pair,
            ),
        )

        pair_distance = current_distances[frozenset({left_name, right_name})]
        delta = (total_distance[left_name] - total_distance[right_name]) / (remaining - 2)
        left_length = max(0.0, 0.5 * (pair_distance + delta))
        right_length = max(0.0, pair_distance - left_length)

        left_node = active_nodes[left_name]
        right_node = active_nodes[right_name]
        merged_name = f"N{next_internal_id}"
        next_internal_id += 1
        merged_node = NJNode(
            name=merged_name,
            left=left_node,
            right=right_node,
            left_length=left_length,
            right_length=right_length,
            members=left_node.members + right_node.members,
        )

        other_names = [
            name
            for name in names
            if name not in {left_name, right_name}
        ]
        for other_name in other_names:
            merged_distance = 0.5 * (
                current_distances[frozenset({left_name, other_name})]
                + current_distances[frozenset({right_name, other_name})]
                - pair_distance
            )
            current_distances[frozenset({merged_name, other_name})] = merged_distance

        active_nodes.pop(left_name)
        active_nodes.pop(right_name)
        active_nodes[merged_name] = merged_node

    final_left_name, final_right_name = list(active_nodes)
    final_distance = current_distances[frozenset({final_left_name, final_right_name})]
    return NJNode(
        name="root",
        left=active_nodes[final_left_name],
        right=active_nodes[final_right_name],
        left_length=final_distance / 2.0,
        right_length=final_distance / 2.0,
        members=active_nodes[final_left_name].members + active_nodes[final_right_name].members,
    )


def to_newick(node: NJNode) -> str:
    """把 NJ 树转成带分支长度的 Newick 字符串。"""

    return _to_newick(node) + ";"


def _to_newick(node: NJNode) -> str:
    """递归生成节点的 Newick 文本。"""

    if node.left is None or node.right is None:
        return node.name

    left_text = _to_newick(node.left)
    right_text = _to_newick(node.right)
    if node.name == "root":
        return f"({left_text}:{node.left_length:.6f},{right_text}:{node.right_length:.6f})"
    return f"({left_text}:{node.left_length:.6f},{right_text}:{node.right_length:.6f}){node.name}"


def _validate_distance_matrix(
    labels: list[str],
    distances: dict[tuple[str, str], float],
) -> None:
    """校验距离矩阵是否合法。"""

    for label in labels:
        if _distance_between(label, label, distances, default=0.0) != 0.0:
            raise ValueError("距离矩阵对角线必须为 0")

    for index, left in enumerate(labels):
        for right in labels[index + 1 :]:
            value = _distance_between(left, right, distances)
            if value < 0.0:
                raise ValueError("距离不能为负数")


def _distance_between(
    left: str,
    right: str,
    distances: dict[tuple[str, str], float],
    default: float | None = None,
) -> float:
    """读取无向距离。"""

    if left == right:
        return 0.0 if default is None else default

    if (left, right) in distances and (right, left) in distances:
        if distances[(left, right)] != distances[(right, left)]:
            raise ValueError("距离矩阵必须对称")
        return distances[(left, right)]
    if (left, right) in distances:
        return distances[(left, right)]
    if (right, left) in distances:
        return distances[(right, left)]
    raise ValueError(f"缺少 {left} 与 {right} 的距离")


if __name__ == "__main__":
    labels = ["A", "B", "C", "D"]
    matrix = {
        ("A", "B"): 5.0,
        ("A", "C"): 9.0,
        ("A", "D"): 9.0,
        ("B", "C"): 10.0,
        ("B", "D"): 10.0,
        ("C", "D"): 8.0,
    }
    root = neighbor_joining_tree(labels, matrix)
    assert root.left is not None and root.right is not None
    assert set(root.members) == {"A", "B", "C", "D"}
    assert "A" in to_newick(root) and "D" in to_newick(root)

    children = {frozenset(root.left.members), frozenset(root.right.members)}
    assert any({"A", "B"}.issubset(child) for child in children)
    assert any({"C", "D"}.issubset(child) for child in children)

    pair_root = neighbor_joining_tree(["X", "Y"], {("X", "Y"): 3.0})
    assert pair_root.left_length == 1.5 and pair_root.right_length == 1.5

    try:
        neighbor_joining_tree(["X", "Y"], {("X", "Y"): -3.0})
        raise AssertionError("负距离应抛出异常")
    except ValueError:
        pass

    print("035_neighbor_joining: all examples passed")
