"""
Rendezvous Hashing（最高随机权重哈希）。

意图：每个 key 对所有节点打分，选择分数最高者；节点变化时只影响必要 key。
"""

from hashlib import sha256


def rendezvous_node(key: str, nodes: list[str]) -> str:
    """为 key 选择得分最高的节点。"""

    if not nodes:
        raise ValueError("nodes 不能为空")
    return max(nodes, key=lambda node: _score(key, node))


def top_k_rendezvous_nodes(key: str, nodes: list[str], k: int) -> list[str]:
    """返回 key 的前 k 个副本节点。"""

    if k < 0:
        raise ValueError("k 不能为负数")
    return sorted(nodes, key=lambda node: _score(key, node), reverse=True)[:k]


def _score(key: str, node: str) -> int:
    digest = sha256(f"{key}|{node}".encode("utf-8")).hexdigest()
    return int(digest, 16)


if __name__ == "__main__":
    nodes = ["n1", "n2", "n3"]
    assert rendezvous_node("alpha", nodes) == "n2"
    assert top_k_rendezvous_nodes("alpha", nodes, 2) == ["n2", "n3"]
    assert top_k_rendezvous_nodes("alpha", nodes, 0) == []

    print("002_rendezvous_hashing: all examples passed")
