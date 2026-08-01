"""
文件意图：手写实现 Aho-Corasick 多模式字符串匹配自动机。
适用场景：在同一文本中搜索大量模式串，例如敏感词扫描、词典匹配与 DNA motif 搜索。
核心思想：Trie 保存模式前缀，失败指针在失配时跳至最长可用后缀状态。
输入输出：构造时输入非空模式串列表，搜索返回 (起始下标, 模式下标) 匹配对。
时间复杂度：构造 O(模式总长度)，搜索 O(文本长度 + 匹配数)。空间复杂度：O(模式总长度)。
关键边界：支持重复模式串；空模式串被拒绝，避免定义为匹配每个文本边界的歧义。
"""

from collections import deque


class _AutomatonNode:
    """Aho-Corasick 内部节点，包含子边、失败指针和本节点结尾的模式编号。"""

    def __init__(self) -> None:
        self.children: dict[str, _AutomatonNode] = {}
        self.failure: _AutomatonNode | None = None
        self.outputs: list[int] = []


class AhoCorasick:
    """面向固定模式集合的手写 Aho-Corasick 自动机。"""

    def __init__(self, patterns: list[str]) -> None:
        """根据 patterns 构建 Trie 和失败指针。

        参数：patterns 为非空模式串列表，可包含重复元素。
        返回：无，随后可调用 search。
        边界情况：空模式集合合法；任一空模式串会抛出 ValueError。
        关键算法点：BFS 保证子节点的失败指针依赖的状态已先构造完成。
        """
        if any(not pattern for pattern in patterns):
            raise ValueError("Aho-Corasick 不支持空模式串")
        self._patterns = patterns[:]
        self._root = _AutomatonNode()
        self._root.failure = self._root
        for pattern_index, pattern in enumerate(patterns):
            node = self._root
            for character in pattern:
                if character not in node.children:
                    node.children[character] = _AutomatonNode()
                node = node.children[character]
            node.outputs.append(pattern_index)
        self._build_failure_links()

    def _build_failure_links(self) -> None:
        """使用 BFS 为所有 Trie 节点建立失败指针并继承输出。"""
        pending: deque[_AutomatonNode] = deque()
        for child in self._root.children.values():
            child.failure = self._root
            pending.append(child)
        while pending:
            node = pending.popleft()
            for character, child in node.children.items():
                failure = node.failure
                while failure is not self._root and character not in failure.children:
                    failure = failure.failure
                if character in failure.children and failure.children[character] is not child:
                    child.failure = failure.children[character]
                else:
                    child.failure = self._root
                # 失败状态结尾的模式也是当前文本后缀中的模式。
                child.outputs.extend(child.failure.outputs)
                pending.append(child)

    def search(self, text: str) -> list[tuple[int, int]]:
        """返回 text 中的全部匹配对 (起始下标, 模式下标)。

        参数：text 为待搜索文本。
        返回：按文本扫描顺序给出的匹配对。
        边界情况：空文本或空模式集合返回空列表。
        关键算法点：每次失败跳转都严格缩短当前候选前缀，因此总搜索时间线性。
        """
        matches: list[tuple[int, int]] = []
        node = self._root
        for index, character in enumerate(text):
            while node is not self._root and character not in node.children:
                node = node.failure
            if character in node.children:
                node = node.children[character]
            else:
                node = self._root
            for pattern_index in node.outputs:
                matches.append((index - len(self._patterns[pattern_index]) + 1, pattern_index))
        return matches


if __name__ == "__main__":
    automaton = AhoCorasick(["he", "she", "his", "hers"])
    assert set(automaton.search("ahishers")) == {(1, 2), (3, 1), (4, 0), (4, 3)}
    assert AhoCorasick(["a", "aa", "a"]).search("aa") == [(0, 0), (0, 2), (0, 1), (1, 0), (1, 2)]
    assert AhoCorasick([]).search("text") == []
    print("005_aho_corasick: all examples passed")
