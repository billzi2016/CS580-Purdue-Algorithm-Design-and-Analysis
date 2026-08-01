"""
文件意图：手写实现 Aho-Corasick 自动机，以一次扫描找出 DNA 序列中的全部 motif 精确命中。
适用场景：同时搜索多个已知短 motif、k-mer 或候选序列片段。
核心思想：Trie 共享模式前缀，失败指针在失配时跳到最长可复用后缀，输出列表沿失败链继承。
输入输出：输入 DNA 文本与互异非空模式列表，输出 (模式, 起点) 命中列表。
时间复杂度：构建 O(模式总长度)，搜索 O(文本长度+命中数)；空间复杂度 O(模式总长度)。
关键边界情况：空文本无命中；空模式或重复模式拒绝；N 按字面字符匹配而不是通配符。
"""

from collections import deque


DNA_ALPHABET = frozenset("ACGTN")


class AhoCorasickMotifMatcher:
    """面向大写 DNA 字符的教学版多模式精确匹配自动机。"""

    def __init__(self, patterns: list[str]) -> None:
        """构建模式 Trie 及其失败指针。

        参数：patterns 是互异、非空的大写 DNA motif 列表。
        返回：无；自动机节点状态存于内部列表。
        边界情况：空列表可构建空自动机；空、重复或非法模式抛出 ValueError。
        关键算法点：BFS 按深度构造失败指针，保证访问节点时其失败节点已准备完毕。
        """
        if len(set(patterns)) != len(patterns) or any(
            not pattern for pattern in patterns
        ):
            raise ValueError("patterns 必须互异且非空")
        for pattern in patterns:
            _validate_dna(pattern, "pattern")
        self.patterns = patterns.copy()
        self.transitions: list[dict[str, int]] = [{}]
        self.failure = [0]
        self.outputs: list[list[int]] = [[]]
        for pattern_index, pattern in enumerate(patterns):
            self._insert(pattern, pattern_index)
        self._build_failure_links()

    def find_all(self, sequence: str) -> list[tuple[str, int]]:
        """返回 sequence 中全部 motif 的 (模式, 零基起点) 命中。

        参数：sequence 是待扫描大写 DNA 序列。
        返回：按文本扫描顺序及模式输出顺序排列的命中列表。
        边界情况：空文本返回空；模式彼此重叠或自重叠时均会完整报告。
        关键算法点：失配时反复跳失败指针，而不回退文本位置，实现单次线性扫描。
        """
        _validate_dna(sequence, "sequence")
        node = 0
        matches: list[tuple[str, int]] = []
        for end, symbol in enumerate(sequence):
            while node and symbol not in self.transitions[node]:
                node = self.failure[node]
            node = self.transitions[node].get(symbol, 0)
            for pattern_index in self.outputs[node]:
                pattern = self.patterns[pattern_index]
                matches.append((pattern, end - len(pattern) + 1))
        return matches

    def _insert(self, pattern: str, pattern_index: int) -> None:
        node = 0
        for symbol in pattern:
            if symbol not in self.transitions[node]:
                self.transitions[node][symbol] = len(self.transitions)
                self.transitions.append({})
                self.failure.append(0)
                self.outputs.append([])
            node = self.transitions[node][symbol]
        self.outputs[node].append(pattern_index)

    def _build_failure_links(self) -> None:
        queue: deque[int] = deque()
        for child in self.transitions[0].values():
            queue.append(child)
        while queue:
            node = queue.popleft()
            for symbol, child in self.transitions[node].items():
                fallback = self.failure[node]
                while fallback and symbol not in self.transitions[fallback]:
                    fallback = self.failure[fallback]
                self.failure[child] = self.transitions[fallback].get(symbol, 0)
                # 后缀模式也在当前位置结束，必须继承其输出以报告重叠命中。
                self.outputs[child].extend(self.outputs[self.failure[child]])
                queue.append(child)


def _validate_dna(sequence: str, name: str) -> None:
    if any(symbol not in DNA_ALPHABET for symbol in sequence):
        raise ValueError(f"{name} 只能包含大写 A、C、G、T 或 N")


if __name__ == "__main__":
    matcher = AhoCorasickMotifMatcher(["AT", "ATA", "TAT"])
    assert matcher.find_all("ATAT") == [("AT", 0), ("ATA", 0), ("TAT", 1), ("AT", 2)]
    assert AhoCorasickMotifMatcher([]).find_all("ACGT") == []
    assert matcher.find_all("") == []
    try:
        AhoCorasickMotifMatcher(["AC", "AC"])
        raise AssertionError("重复模式应抛出 ValueError")
    except ValueError:
        pass
    print("004_aho_corasick_motif_matching: all examples passed")
