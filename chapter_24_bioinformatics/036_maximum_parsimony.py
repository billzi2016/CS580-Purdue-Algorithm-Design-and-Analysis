"""固定树拓扑上的 Fitch 最大简约评分教学实现。

适用场景：
- 已知一棵二叉树拓扑和叶子序列；
- 需要评估该拓扑在 maximum parsimony 准则下的最小替换次数；
- 适合作为系统发育树打分基础，而不是完整的树搜索器。

核心思想：
- 对每个位点自底向上做 Fitch 集合递推；
- 左右子树集合有交集时，父节点集合取交集且不加分；
- 无交集时，父节点集合取并集并把该位点代价加 1；
- 全位点代价求和得到该固定拓扑的简约分数。

输入输出：
- 输入：树根节点与叶子到序列的映射；
- 输出：总 parsimony 分数，以及每个内部节点的一个可行祖先序列。

时间复杂度：O(L * V)
空间复杂度：O(L * V)

关键边界情况：
- 序列长度必须一致；
- 叶子必须全部出现在序列字典中；
- 这是“固定拓扑打分版”，不是在所有可能树中搜索全局最优树。
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ParsimonyNode:
    """Fitch 打分用树节点。"""

    name: str
    left: ParsimonyNode | None = None
    right: ParsimonyNode | None = None


@dataclass(frozen=True)
class ParsimonyResult:
    """固定拓扑的最大简约结果。"""

    score: int
    ancestral_sequences: dict[str, str]


def fitch_parsimony(
    root: ParsimonyNode, leaf_sequences: dict[str, str]
) -> ParsimonyResult:
    """计算固定二叉树拓扑的 Fitch 简约分数。

    参数：
    - root：树根节点；
    - leaf_sequences：叶子名到等长序列的映射。

    返回值：
    - `ParsimonyResult`，包含总分和一个可行的内部节点祖先序列赋值。

    边界情况：
    - 空序列、长度不一致、缺叶子或非二叉内部节点都会抛出异常；
    - 单叶树的分数为 0。

    关键算法点：
    - 每个位点单独应用 Fitch 递推；
    - 祖先序列不是唯一解，这里只取每个位点集合中字典序最小的字符作为一个教学版可行赋值。
    """

    leaf_names = _collect_leaf_names(root)
    if not leaf_names:
        raise ValueError("树至少要包含一个叶子")
    if set(leaf_sequences) != leaf_names:
        raise ValueError("leaf_sequences 必须与树叶子集合完全一致")

    sequence_length = len(next(iter(leaf_sequences.values())))
    if sequence_length == 0:
        raise ValueError("叶子序列不能为空")
    if any(len(sequence) != sequence_length for sequence in leaf_sequences.values()):
        raise ValueError("所有叶子序列长度必须一致")

    internal_node_names = {
        node_name
        for node_name in _collect_all_node_names(root)
        if node_name not in leaf_names
    }
    internal_assignments: dict[str, list[str]] = {}
    total_score = 0

    for column in range(sequence_length):
        site_sets: dict[str, set[str]] = {}
        total_score += _fitch_site(root, leaf_sequences, column, site_sets)

        for node_name, character_set in site_sets.items():
            if node_name not in internal_node_names:
                continue
            internal_assignments.setdefault(node_name, []).append(min(character_set))

    return ParsimonyResult(
        score=total_score,
        ancestral_sequences={
            node_name: "".join(characters)
            for node_name, characters in internal_assignments.items()
        },
    )


def _fitch_site(
    node: ParsimonyNode,
    leaf_sequences: dict[str, str],
    column: int,
    site_sets: dict[str, set[str]],
) -> int:
    """对单个位点执行 Fitch 自底向上递推。"""

    if node.left is None and node.right is None:
        site_sets[node.name] = {leaf_sequences[node.name][column]}
        return 0
    if node.left is None or node.right is None:
        raise ValueError("内部节点必须恰好有两个孩子")

    left_cost = _fitch_site(node.left, leaf_sequences, column, site_sets)
    right_cost = _fitch_site(node.right, leaf_sequences, column, site_sets)
    intersection = site_sets[node.left.name] & site_sets[node.right.name]

    # 有交集时不需要引入新的替换；无交集才把代价加 1。
    if intersection:
        site_sets[node.name] = intersection
        return left_cost + right_cost

    site_sets[node.name] = site_sets[node.left.name] | site_sets[node.right.name]
    return left_cost + right_cost + 1


def _collect_leaf_names(node: ParsimonyNode) -> set[str]:
    """收集树上所有叶子名称。"""

    if node.left is None and node.right is None:
        return {node.name}
    if node.left is None or node.right is None:
        raise ValueError("内部节点必须恰好有两个孩子")
    return _collect_leaf_names(node.left) | _collect_leaf_names(node.right)


def _collect_all_node_names(node: ParsimonyNode) -> set[str]:
    """收集树上所有节点名称。"""

    names = {node.name}
    if node.left is not None:
        names |= _collect_all_node_names(node.left)
    if node.right is not None:
        names |= _collect_all_node_names(node.right)
    return names


if __name__ == "__main__":
    tree = ParsimonyNode(
        "root",
        left=ParsimonyNode("AB", left=ParsimonyNode("A"), right=ParsimonyNode("B")),
        right=ParsimonyNode("CD", left=ParsimonyNode("C"), right=ParsimonyNode("D")),
    )
    sequences = {
        "A": "AAA",
        "B": "AAT",
        "C": "GGA",
        "D": "GGT",
    }
    result = fitch_parsimony(tree, sequences)
    assert result.score == 4
    assert result.ancestral_sequences["AB"] == "AAA"
    assert result.ancestral_sequences["CD"] == "GGA"
    assert result.ancestral_sequences["root"] == "AAA"
    assert set(result.ancestral_sequences) == {"AB", "CD", "root"}

    single = fitch_parsimony(ParsimonyNode("leaf"), {"leaf": "AC"})
    assert single.score == 0

    try:
        fitch_parsimony(tree, {"A": "A", "B": "A", "C": "A", "D": "AA"})
        raise AssertionError("长度不一致应抛出异常")
    except ValueError:
        pass

    print("036_maximum_parsimony: all examples passed")
