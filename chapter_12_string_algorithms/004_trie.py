"""
文件意图：手写实现字符 Trie（前缀树）。
适用场景：维护动态词典，并高效判断完整单词或任意前缀是否存在。
核心思想：共享相同前缀的单词路径，每条边表示一个字符，终止标记区分前缀和完整单词。
输入输出：插入字符串后，可查询单词和前缀是否存在。
时间复杂度：插入、查询均为 O(L)。空间复杂度：O(所有已插入字符数)。
关键边界：支持空字符串，将根节点标记为一个完整单词。
"""


class _TrieNode:
    """Trie 内部节点，保存子边和单词终止标记。"""

    def __init__(self) -> None:
        self.children: dict[str, _TrieNode] = {}
        self.is_word = False


class Trie:
    """支持插入、完整匹配和前缀匹配的手写 Trie。"""

    def __init__(self) -> None:
        """创建空 Trie；根节点同时代表空前缀。"""
        self._root = _TrieNode()

    def insert(self, word: str) -> None:
        """把 word 插入 Trie。

        参数：word 为要插入的任意字符串。
        返回：无。
        边界情况：空字符串会标记根节点，不影响其他单词。
        关键算法点：已有前缀路径复用原节点，只为缺失字符创建新节点。
        """
        node = self._root
        for character in word:
            if character not in node.children:
                node.children[character] = _TrieNode()
            node = node.children[character]
        node.is_word = True

    def contains(self, word: str) -> bool:
        """判断 word 是否作为完整单词存在。

        参数：word 为待查字符串。
        返回：仅在路径存在且末节点有终止标记时返回 True。
        边界情况：空字符串取决于它是否曾被插入。
        关键算法点：单词终止标记避免把长单词的前缀误判为完整单词。
        """
        node = self._find_node(word)
        return node is not None and node.is_word

    def starts_with(self, prefix: str) -> bool:
        """判断 Trie 中是否存在以 prefix 开头的单词。

        参数：prefix 为待查前缀。
        返回：前缀路径存在时返回 True。
        边界情况：空前缀总存在。
        关键算法点：此查询只要求路径存在，不要求终止标记。
        """
        return self._find_node(prefix) is not None

    def _find_node(self, text: str) -> _TrieNode | None:
        """沿 text 路径定位节点；路径缺失时返回 None。"""
        node = self._root
        for character in text:
            if character not in node.children:
                return None
            node = node.children[character]
        return node


if __name__ == "__main__":
    trie = Trie()
    trie.insert("apple")
    trie.insert("app")
    trie.insert("")
    assert trie.contains("apple")
    assert trie.contains("app")
    assert not trie.contains("ap")
    assert trie.starts_with("ap") and not trie.starts_with("bat")
    assert trie.contains("")
    print("004_trie: all examples passed")
