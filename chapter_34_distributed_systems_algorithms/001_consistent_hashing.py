"""
Consistent Hashing：把节点和 key 放到同一个哈希环上。

意图：展示分布式缓存/分片在节点增删时如何减少 key 迁移。
"""

from bisect import bisect_left, insort
from hashlib import md5


class ConsistentHashRing:
    """带虚拟节点的一致性哈希环。"""

    def __init__(self, replicas: int = 3) -> None:
        if replicas <= 0:
            raise ValueError("replicas 必须为正数")
        self.replicas = replicas
        self.ring: list[int] = []
        self.owners: dict[int, str] = {}

    def add_node(self, node: str) -> None:
        """加入物理节点及其虚拟节点。"""

        for replica in range(self.replicas):
            token = self._hash(f"{node}#{replica}")
            if token not in self.owners:
                insort(self.ring, token)
                self.owners[token] = node

    def remove_node(self, node: str) -> None:
        """删除节点的所有虚拟节点。"""

        tokens = [token for token, owner in self.owners.items() if owner == node]
        for token in tokens:
            self.ring.remove(token)
            del self.owners[token]

    def get_node(self, key: str) -> str:
        """返回 key 顺时针遇到的第一个节点。"""

        if not self.ring:
            raise ValueError("哈希环为空")
        token = self._hash(key)
        index = bisect_left(self.ring, token) % len(self.ring)
        return self.owners[self.ring[index]]

    def _hash(self, value: str) -> int:
        return int(md5(value.encode("utf-8")).hexdigest(), 16)


if __name__ == "__main__":
    ring = ConsistentHashRing(replicas=5)
    for node in ["A", "B", "C"]:
        ring.add_node(node)
    assert ring.get_node("user:1") in {"A", "B", "C"}
    before = ring.get_node("user:2")
    ring.remove_node(before)
    assert ring.get_node("user:2") in {"A", "B", "C"} - {before}

    print("001_consistent_hashing: all examples passed")
