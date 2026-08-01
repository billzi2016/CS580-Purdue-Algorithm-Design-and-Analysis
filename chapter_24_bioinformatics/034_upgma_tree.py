"""UPGMA 系统发育树的教学实现。

适用场景：
- 输入是一组样本之间的对称距离矩阵；
- 假设分子钟成立，也就是各分支演化速率近似一致；
- 需要构建一棵 rooted ultrametric tree 作为层次聚类结果。

核心思想：
- 初始时每个样本都是一个单独 cluster；
- 每轮选出平均距离最小的两个 cluster 合并；
- 新 cluster 到其他 cluster 的距离按成员数加权平均更新；
- 合并高度等于被合并两簇距离的一半，因此最终树是 ultrametric 的。

输入输出：
- 输入：样本标签列表与样本间距离字典；
- 输出：一棵带高度信息的 rooted tree。

时间复杂度：O(n^3)
空间复杂度：O(n^2)

关键边界情况：
- 空标签列表会抛出异常；
- 单个样本返回单节点树；
- 距离矩阵必须对称、非负、对角线为 0；
- 这是教学版 UPGMA，不处理缺失距离、并列最优随机打破或工业级优化。
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class UPGMANode:
    """UPGMA 树节点。"""

    name: str
    height: float
    members: tuple[str, ...]
    left: UPGMANode | None = None
    right: UPGMANode | None = None


def upgma_tree(labels: list[str], distances: dict[tuple[str, str], float]) -> UPGMANode:
    """根据距离矩阵构建 UPGMA 系统发育树。

    参数：
    - labels：叶子标签列表；
    - distances：无向距离矩阵，键使用 `(a, b)` 二元组表示。

    返回值：
    - UPGMA 根节点。

    边界情况：
    - 标签为空时抛出异常；
    - 只有一个标签时返回单叶节点；
    - 缺少任意一对距离、距离非对称或为负时抛出异常。

    关键算法点：
    - 合并后新簇与外部簇的距离必须按簇大小加权平均，而不是简单平均；
    - 节点高度使用簇间距离的一半，这样根到所有叶子的路径长度一致。
    """

    if not labels:
        raise ValueError("labels 不能为空")
    if len(set(labels)) != len(labels):
        raise ValueError("labels 不能包含重复项")

    _validate_distance_matrix(labels, distances)

    clusters: dict[str, UPGMANode] = {
        label: UPGMANode(name=label, height=0.0, members=(label,))
        for label in labels
    }
    cluster_distances = {
        frozenset({left, right}): _distance_between(left, right, distances)
        for index, left in enumerate(labels)
        for right in labels[index + 1 :]
    }
    next_internal_id = 1

    while len(clusters) > 1:
        left_name, right_name = min(
            (
                tuple(pair)
                for pair in cluster_distances
                if pair.issubset(clusters)
            ),
            key=lambda pair: (
                cluster_distances[frozenset(pair)],
                sorted(pair),
            ),
        )

        left_cluster = clusters[left_name]
        right_cluster = clusters[right_name]
        merged_distance = cluster_distances[frozenset({left_name, right_name})]
        merged_height = merged_distance / 2.0
        merged_name = f"U{next_internal_id}"
        next_internal_id += 1

        merged_cluster = UPGMANode(
            name=merged_name,
            height=merged_height,
            members=left_cluster.members + right_cluster.members,
            left=left_cluster,
            right=right_cluster,
        )

        other_names = [
            cluster_name
            for cluster_name in clusters
            if cluster_name not in {left_name, right_name}
        ]

        for other_name in other_names:
            left_distance = cluster_distances[frozenset({left_name, other_name})]
            right_distance = cluster_distances[frozenset({right_name, other_name})]
            weighted_distance = (
                left_distance * len(left_cluster.members)
                + right_distance * len(right_cluster.members)
            ) / (len(left_cluster.members) + len(right_cluster.members))
            cluster_distances[frozenset({merged_name, other_name})] = weighted_distance

        clusters.pop(left_name)
        clusters.pop(right_name)
        clusters[merged_name] = merged_cluster

    return next(iter(clusters.values()))


def to_newick(node: UPGMANode) -> str:
    """把 UPGMA 树转成带分支长度的 Newick 字符串。"""

    return _node_to_newick(node, parent_height=node.height) + ";"


def _node_to_newick(node: UPGMANode, parent_height: float) -> str:
    """递归生成当前节点的 Newick 片段。"""

    branch_length = parent_height - node.height
    if node.left is None or node.right is None:
        return f"{node.name}:{branch_length:.6f}"

    left_text = _node_to_newick(node.left, node.height)
    right_text = _node_to_newick(node.right, node.height)
    return f"({left_text},{right_text}){node.name}:{branch_length:.6f}"


def _validate_distance_matrix(
    labels: list[str],
    distances: dict[tuple[str, str], float],
) -> None:
    """校验距离矩阵是否合法。"""

    for label in labels:
        diagonal = _distance_between(label, label, distances, default=0.0)
        if diagonal != 0.0:
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
    """读取无向距离矩阵中的一个值。"""

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
        ("A", "B"): 2.0,
        ("A", "C"): 8.0,
        ("A", "D"): 8.0,
        ("B", "C"): 8.0,
        ("B", "D"): 8.0,
        ("C", "D"): 2.0,
    }
    root = upgma_tree(labels, matrix)
    assert set(root.members) == {"A", "B", "C", "D"}
    assert root.height == 4.0
    assert root.left is not None and root.right is not None
    assert {frozenset(root.left.members), frozenset(root.right.members)} == {
        frozenset({"A", "B"}),
        frozenset({"C", "D"}),
    }
    assert "A" in to_newick(root) and "D" in to_newick(root)

    single = upgma_tree(["X"], {})
    assert single.name == "X" and single.height == 0.0

    try:
        upgma_tree(["A", "B"], {("A", "B"): -1.0})
        raise AssertionError("负距离应抛出异常")
    except ValueError:
        pass

    print("034_upgma_tree: all examples passed")
