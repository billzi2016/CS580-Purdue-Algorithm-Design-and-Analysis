"""
文件意图：
    本文件手写实现树形 DP，以树上最大独立集为例。

适用场景：
    状态依赖父子关系且原图是树或森林的问题。

核心思想：
    对每个节点维护两个状态：选择该节点、不选择该节点。选择当前节点时不能选择子节点；
    不选择当前节点时，每个子节点可选可不选，取较优。

时间复杂度：
    O(V)

空间复杂度：
    O(V)
"""

from collections.abc import Hashable

Node = Hashable
Tree = dict[Node, list[Node]]


def maximum_independent_set_size(tree: Tree, root: Node) -> int:
    """返回以 root 所在树为范围的最大独立集大小。"""
    include, exclude = _dfs(tree, root, None)
    return max(include, exclude)


def _dfs(tree: Tree, node: Node, parent: Node | None) -> tuple[int, int]:
    """返回 (选择 node 的最优值, 不选择 node 的最优值)。"""
    include = 1
    exclude = 0
    for child in tree.get(node, []):
        if child == parent:
            continue
        child_include, child_exclude = _dfs(tree, child, node)
        include += child_exclude
        exclude += max(child_include, child_exclude)
    return include, exclude


if __name__ == "__main__":
    tree = {
        1: [2, 3],
        2: [1, 4, 5],
        3: [1],
        4: [2],
        5: [2],
    }
    assert maximum_independent_set_size(tree, 1) == 3
    assert maximum_independent_set_size({1: []}, 1) == 1
    assert maximum_independent_set_size({"A": ["B"], "B": ["A"]}, "A") == 1

    print("002_tree_dp: all examples passed")
