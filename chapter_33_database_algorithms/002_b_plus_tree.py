"""
B+ tree 基础实现：内部节点只导航，叶子节点保存 key-value 并通过链表相连。

意图：展示数据库范围扫描为什么偏好 B+ tree。这里实现插入、点查和范围查询。
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class BPlusNode:
    """B+ tree 节点。"""

    leaf: bool
    keys: list[int] = field(default_factory=list)
    children: list["BPlusNode"] = field(default_factory=list)
    values: list[Any] = field(default_factory=list)
    next_leaf: "BPlusNode | None" = None


class BPlusTree:
    """小型 B+ tree，order 表示一个节点最多容纳多少 key。"""

    def __init__(self, order: int = 3) -> None:
        if order < 3:
            raise ValueError("order 至少为 3")
        self.order = order
        self.root = BPlusNode(True)

    def search(self, key: int) -> Any | None:
        """点查 key 对应 value。"""

        leaf = self._find_leaf(key)
        for index, existing in enumerate(leaf.keys):
            if existing == key:
                return leaf.values[index]
        return None

    def insert(self, key: int, value: Any) -> None:
        """插入或覆盖 key-value。"""

        leaf = self._find_leaf(key)
        for index, existing in enumerate(leaf.keys):
            if existing == key:
                leaf.values[index] = value
                return
        position = 0
        while position < len(leaf.keys) and leaf.keys[position] < key:
            position += 1
        leaf.keys.insert(position, key)
        leaf.values.insert(position, value)
        if len(leaf.keys) >= self.order:
            promoted, right = self._split_leaf(leaf)
            if leaf is self.root:
                self.root = BPlusNode(False, [promoted], [leaf, right])
            else:
                self._insert_into_parent(self.root, leaf, promoted, right)

    def range_query(self, left: int, right: int) -> list[Any]:
        """返回 key 位于 [left, right] 的 value，按 key 升序。"""

        result: list[Any] = []
        leaf = self._find_leaf(left)
        while leaf:
            for key, value in zip(leaf.keys, leaf.values, strict=True):
                if key > right:
                    return result
                if key >= left:
                    result.append(value)
            leaf = leaf.next_leaf
        return result

    def _find_leaf(self, key: int) -> BPlusNode:
        node = self.root
        while not node.leaf:
            index = 0
            while index < len(node.keys) and key >= node.keys[index]:
                index += 1
            node = node.children[index]
        return node

    def _split_leaf(self, leaf: BPlusNode) -> tuple[int, BPlusNode]:
        mid = len(leaf.keys) // 2
        right = BPlusNode(True, leaf.keys[mid:], values=leaf.values[mid:])
        leaf.keys = leaf.keys[:mid]
        leaf.values = leaf.values[:mid]
        right.next_leaf = leaf.next_leaf
        leaf.next_leaf = right
        return right.keys[0], right

    def _insert_into_parent(
        self, node: BPlusNode, left: BPlusNode, key: int, right: BPlusNode
    ) -> bool:
        if node.leaf:
            return False
        for index, child in enumerate(node.children):
            if child is left:
                node.keys.insert(index, key)
                node.children.insert(index + 1, right)
                return True
            if self._insert_into_parent(child, left, key, right):
                if len(child.keys) >= self.order:
                    promoted, new_right = self._split_internal(child)
                    node.keys.insert(index, promoted)
                    node.children.insert(index + 1, new_right)
                if len(self.root.keys) >= self.order:
                    promoted, new_right = self._split_internal(self.root)
                    self.root = BPlusNode(False, [promoted], [self.root, new_right])
                return True
        return False

    def _split_internal(self, node: BPlusNode) -> tuple[int, BPlusNode]:
        mid = len(node.keys) // 2
        promoted = node.keys[mid]
        right = BPlusNode(False, node.keys[mid + 1 :], node.children[mid + 1 :])
        node.keys = node.keys[:mid]
        node.children = node.children[: mid + 1]
        return promoted, right


if __name__ == "__main__":
    tree = BPlusTree(order=3)
    for key in [5, 1, 9, 3, 7]:
        tree.insert(key, f"v{key}")
    assert tree.search(3) == "v3"
    assert tree.search(4) is None
    assert tree.range_query(3, 8) == ["v3", "v5", "v7"]

    print("002_b_plus_tree: all examples passed")
