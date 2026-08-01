"""graph indexing 基础教学实现。

适用场景：对图中所有短路径片段建立索引，支持后续图上精确匹配或 seed lookup。
核心思想：枚举 DAG 上长度不超过 k 的路径标签，把片段映射到起点节点与路径字符串。
输入输出：输入图节点、边和 k；输出片段到起始节点列表的倒排索引。
时间复杂度：与枚举路径片段数成正比；教学版不适合高分支真实泛基因组。
关键边界情况：这里只做 DAG 深度优先展开；节点标签允许多字符；片段长度不足 k 时不输出。
"""


def build_graph_kmer_index(node_labels: dict[str, str], edges: dict[str, list[str]], starts: list[str], k: int) -> dict[str, list[str]]:
    """从给定起点集合构建图上 k-mer 倒排索引。"""

    if k <= 0:
        raise ValueError("k 必须为正整数")
    index: dict[str, list[str]] = {}
    for start in starts:
        _dfs_collect(node_labels, edges, start, k, "", start, index)
    for token in index:
        index[token] = sorted(set(index[token]))
    return index


def _dfs_collect(
    node_labels: dict[str, str],
    edges: dict[str, list[str]],
    node_id: str,
    k: int,
    prefix: str,
    origin: str,
    index: dict[str, list[str]],
) -> None:
    sequence = prefix + node_labels[node_id]
    if len(sequence) >= k:
        for offset in range(len(sequence) - k + 1):
            index.setdefault(sequence[offset : offset + k], []).append(origin)
    for target in edges.get(node_id, []):
        _dfs_collect(node_labels, edges, target, k, sequence[-(k - 1) :] if k > 1 else "", origin, index)


if __name__ == "__main__":
    node_labels = {"n1": "AC", "n2": "G", "n3": "T"}
    edges = {"n1": ["n2", "n3"], "n2": [], "n3": []}
    index = build_graph_kmer_index(node_labels, edges, ["n1"], 3)
    assert index["ACG"] == ["n1"]
    assert index["ACT"] == ["n1"]
    print("044_graph_indexing_basics: all examples passed")
