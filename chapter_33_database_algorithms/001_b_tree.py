"""
B-tree 基础实现：多路平衡搜索树。

意图：展示数据库索引中“一个节点存多个 key、降低树高、适配磁盘页”的核心思想。
这里实现最小度数 t 的插入和查找；删除会显著拉长代码，放在后续高级版本中。
"""

from dataclasses import dataclass, field


@dataclass
class BTreeNode:
    """B-tree 节点；leaf 表示是否叶子，keys 保持升序。"""

    leaf: bool
    keys: list[int] = field(default_factory=list)
    children: list["BTreeNode"] = field(default_factory=list)


class BTree:
    """最小度数为 t 的 B-tree。"""

    def __init__(self, minimum_degree: int = 2) -> None:
        if minimum_degree < 2:
            raise ValueError("minimum_degree 至少为 2")
        self.t = minimum_degree
        self.root = BTreeNode(True)

    def search(self, key: int) -> bool:
        """判断 key 是否存在。"""

        return self._search(self.root, key)

    def insert(self, key: int) -> None:
        """插入 key；为便于教学，重复 key 会被忽略。"""

        if self.search(key):
            return
        root = self.root
        if len(root.keys) == 2 * self.t - 1:
            new_root = BTreeNode(False, children=[root])
            self._split_child(new_root, 0)
            self.root = new_root
        self._insert_non_full(self.root, key)

    def inorder(self) -> list[int]:
        """返回所有 key 的升序遍历。"""

        result: list[int] = []
        self._inorder(self.root, result)
        return result

    def _search(self, node: BTreeNode, key: int) -> bool:
        index = 0
        while index < len(node.keys) and key > node.keys[index]:
            index += 1
        if index < len(node.keys) and key == node.keys[index]:
            return True
        if node.leaf:
            return False
        return self._search(node.children[index], key)

    def _split_child(self, parent: BTreeNode, child_index: int) -> None:
        """拆分满子节点，并把中位 key 提升到 parent。"""

        full = parent.children[child_index]
        sibling = BTreeNode(full.leaf)
        median = full.keys[self.t - 1]
        sibling.keys = full.keys[self.t :]
        full.keys = full.keys[: self.t - 1]
        if not full.leaf:
            sibling.children = full.children[self.t :]
            full.children = full.children[: self.t]
        parent.keys.insert(child_index, median)
        parent.children.insert(child_index + 1, sibling)

    def _insert_non_full(self, node: BTreeNode, key: int) -> None:
        index = len(node.keys) - 1
        if node.leaf:
            node.keys.append(0)
            while index >= 0 and key < node.keys[index]:
                node.keys[index + 1] = node.keys[index]
                index -= 1
            node.keys[index + 1] = key
            return
        while index >= 0 and key < node.keys[index]:
            index -= 1
        index += 1
        if len(node.children[index].keys) == 2 * self.t - 1:
            self._split_child(node, index)
            if key > node.keys[index]:
                index += 1
        self._insert_non_full(node.children[index], key)

    def _inorder(self, node: BTreeNode, result: list[int]) -> None:
        for index, key in enumerate(node.keys):
            if not node.leaf:
                self._inorder(node.children[index], result)
            result.append(key)
        if not node.leaf:
            self._inorder(node.children[-1], result)


if __name__ == "__main__":
    tree = BTree(2)
    for value in [10, 20, 5, 6, 12, 30, 7, 17]:
        tree.insert(value)
    assert tree.inorder() == [5, 6, 7, 10, 12, 17, 20, 30]
    assert tree.search(12)
    assert not tree.search(99)

    print("001_b_tree: all examples passed")
