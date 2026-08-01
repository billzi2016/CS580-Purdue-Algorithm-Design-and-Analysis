"""sequence-to-graph alignment 教学实现。

适用场景：把读段序列与 variation graph 或 DAG 参考对齐，而不是只对齐到单条线性序列。
核心思想：在图的拓扑顺序上做动态规划；每个节点标签与 query 做局部 Smith-Waterman 风格更新。
输入输出：输入 DAG 形式图、query 和简单打分参数；输出最佳得分和终止位置。
时间复杂度：教学版 O(|V| * |query| + |E| * |query|)，空间复杂度 O(|V| * |query|)。
关键边界情况：这里只实现单字符节点标签；图必须是 DAG 且提供拓扑顺序；不回溯具体 CIGAR。
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class AlignmentResult:
    """最佳局部图对齐结果。"""

    score: int
    end_node: str
    end_query_index: int


def sequence_to_graph_alignment(
    node_labels: dict[str, str],
    predecessors: dict[str, list[str]],
    topological_order: list[str],
    query: str,
    match_score: int = 2,
    mismatch_penalty: int = -1,
    gap_penalty: int = -1,
) -> AlignmentResult:
    """在 DAG 图上做简化局部对齐。"""

    if any(len(label) != 1 for label in node_labels.values()):
        raise ValueError("教学版只支持单字符节点标签")
    if not topological_order:
        raise ValueError("topological_order 不能为空")
    dp = {node_id: [0] * (len(query) + 1) for node_id in topological_order}
    best = AlignmentResult(0, topological_order[0], 0)
    for node_id in topological_order:
        label = node_labels[node_id]
        parents = predecessors.get(node_id, [])
        for query_index in range(1, len(query) + 1):
            diagonal_sources = (
                [dp[parent][query_index - 1] for parent in parents] if parents else [0]
            )
            left_sources = (
                [dp[parent][query_index] for parent in parents] if parents else [0]
            )
            diagonal = max(diagonal_sources)
            vertical = max(left_sources)
            score = max(
                0,
                diagonal
                + (
                    match_score if label == query[query_index - 1] else mismatch_penalty
                ),
                dp[node_id][query_index - 1] + gap_penalty,
                vertical + gap_penalty,
            )
            dp[node_id][query_index] = score
            if score > best.score:
                best = AlignmentResult(score, node_id, query_index)
    return best


if __name__ == "__main__":
    node_labels = {"n1": "A", "n2": "C", "n3": "T"}
    predecessors = {"n1": [], "n2": ["n1"], "n3": ["n1"]}
    result = sequence_to_graph_alignment(
        node_labels, predecessors, ["n1", "n2", "n3"], "ACT"
    )
    assert result.score >= 4
    assert result.end_node in {"n2", "n3"}
    print("043_sequence_to_graph_alignment: all examples passed")
